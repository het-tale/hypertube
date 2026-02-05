import httpx
from typing import List, Optional
from datetime import datetime

class ArchiveOrgService:
    """Service for searching and fetching torrents from Archive.org"""
    
    BASE_URL = "https://archive.org"
    SEARCH_URL = f"{BASE_URL}/advancedsearch.php"
    DETAILS_URL = f"{BASE_URL}/metadata"
    # DETAILS_URL = f"{BASE_URL}/details"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_movies(
        self, 
        query: str, 
        page: int = 1, 
        limit: int = 20
    ) -> List[dict]:
        """
        Search for movies on Archive.org
        
        Args:
            query: Search term (e.g., "night of the living dead")
            page: Page number
            limit: Results per page
        
        Returns:
            List of movie metadata with torrent links
        """
        params = {
            # Search in movies collection
            "q": f"({query}) AND mediatype:movies",
            
            # Return fields
            "fl[]": [
                "identifier",  # Unique ID
                "title",
                "description",
                "year",
                "runtime",
                "creator",
                "subject",  # Genres/tags
                "downloads",  # Popularity indicator
                "avg_rating",
                "num_reviews",
            ],
            
            # Pagination
            "rows": limit,
            "page": page,
            
            # Sort by relevance or popularity
            "sort[]": "downloads desc",
            
            # Return as JSON
            "output": "json",
        }
        
        try:
            response = await self.client.get(self.SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process results
            movies = []
            for doc in data.get("response", {}).get("docs", []):
                movie = await self._process_search_result(doc)
                if movie:
                    movies.append(movie)
            
            return movies
            
        except Exception as e:
            print(f"Archive.org search error: {e}")
            return []
    
    async def _process_search_result(self, doc: dict) -> Optional[dict]:
        """Convert Archive.org document to our movie format"""
        
        identifier = doc.get("identifier")
        if not identifier:
            return None
        
        # Get torrent link
        torrent_url = f"{self.BASE_URL}/download/{identifier}/{identifier}_archive.torrent"
        
        # Get poster/thumbnail
        poster_url = f"{self.BASE_URL}/services/img/{identifier}"
        
        # Parse year
        year = None
        year_str = doc.get("year")
        if year_str:
            try:
                if isinstance(year_str, list):
                    year = int(year_str[0])
                else:
                    year = int(year_str)
            except (ValueError, TypeError):
                pass
        
        # Parse genres from subjects
        genres = []
        subjects = doc.get("subject", [])
        if isinstance(subjects, str):
            subjects = [subjects]
        genres = subjects[:5]  # Limit to 5 genres
        
        # Parse runtime (Archive.org stores in seconds as string)
        runtime = None
        runtime_str = doc.get("runtime")
        if runtime_str:
            try:
                # Runtime might be "1:32:45" or "5565" (seconds)
                if isinstance(runtime_str, list):
                    runtime_str = runtime_str[0]
                
                if ":" in runtime_str:
                    # Parse "HH:MM:SS" or "MM:SS"
                    parts = runtime_str.split(":")
                    if len(parts) == 3:
                        h, m, s = parts
                        runtime = int(h) * 3600 + int(m) * 60 + int(s)
                    elif len(parts) == 2:
                        m, s = parts
                        runtime = int(m) * 60 + int(s)
                else:
                    runtime = int(float(runtime_str))
            except (ValueError, TypeError):
                pass
        
        return {
            "id": identifier,
            "title": doc.get("title", "Unknown"),
            "year": year,
            "runtime": runtime,  # in seconds
            "rating": doc.get("avg_rating"),
            "description": doc.get("description", ""),
            "director": doc.get("creator", [None])[0] if doc.get("creator") else None,
            "genres": genres,
            "poster_url": poster_url,
            "source": "archive.org",
            
            # Torrent info
            "torrents": [
                {
                    "quality": "Original",  # Archive.org provides original quality
                    "torrent_url": torrent_url,
                    "magnet_link": None,  # We'll generate from torrent file if needed
                    "seeders": None,  # Archive.org doesn't provide this
                    "leechers": None,
                    "size_bytes": None,  # Would need to fetch torrent file to know
                    "file_format": "various",  # Archive.org has multiple formats
                }
            ],
            
            # Additional metadata
            "downloads": doc.get("downloads", 0),
            "num_reviews": doc.get("num_reviews", 0),
            "archive_url": f"{self.BASE_URL}/details/{identifier}",
        }
    
    async def get_movie_details(self, identifier: str) -> Optional[dict]:
        """
        Get detailed information about a specific movie
        
        Args:
            identifier: Archive.org identifier
        
        Returns:
            Detailed movie metadata with torrent info
        """
        try:
            # Get metadata
            response = await self.client.get(f"{self.DETAILS_URL}/{identifier}")
            response.raise_for_status()
            data = response.json()
            
            metadata = data.get("metadata", {})
            files = data.get("files", [])
            
            # Find video files
            video_files = [
                f for f in files
                if f.get("format") in ["MPEG4", "h.264", "Ogg Video", "Matroska"]
            ]
            
            # Get the best quality video file
            best_video = None
            if video_files:
                # Sort by size (larger = better quality usually)
                video_files.sort(key=lambda x: int(x.get("size", 0)), reverse=True)
                best_video = video_files[0]
            
            # Build torrent info
            torrents = []
            torrent_url = f"{self.BASE_URL}/download/{identifier}/{identifier}_archive.torrent"
            
            if best_video:
                torrents.append({
                    "quality": "Original",
                    "torrent_url": torrent_url,
                    "size_bytes": int(best_video.get("size", 0)),
                    "file_format": best_video.get("format"),
                    "filename": best_video.get("name"),
                })
            return data
            return {
                "id": identifier,
                "title": metadata.get("title", "Unknown"),
                "year": metadata.get("year"),
                "description": metadata.get("description", ""),
                "director": metadata.get("director"),
                "runtime": metadata.get("runtime"),
                "genres": metadata.get("subject", []),
                "poster_url": f"{self.BASE_URL}/services/img/{identifier}",
                "torrents": torrents,
                "archive_url": f"{self.BASE_URL}/details/{identifier}",
                "source": "archive.org",
            }
            
        except Exception as e:
            print(f"Error fetching Archive.org details: {e}")
            return None
    
    async def get_torrent_file(self, identifier: str) -> Optional[bytes]:
        """Download the .torrent file for a movie"""
        try:
            torrent_url = f"{self.BASE_URL}/download/{identifier}/{identifier}_archive.torrent"
            response = await self.client.get(torrent_url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error downloading torrent: {e}")
            return None
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()