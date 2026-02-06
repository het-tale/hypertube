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
        q = f"({query}) AND mediatype:movies" if query else "mediatype:movies"
        params = {
            # Search in movies collection
            "q": q,
            # "q": f"({query}) AND mediatype:movies AND language:French",  # Added language filter for better results
            # "q": f"title:(hello) AND mediatype:(movies) AND language:(French)",  # Added language filter for better results
            
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
            "sort[]": "week desc, downloads desc",
            
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
            print(f"Archive.org search for '{query}' returned {len(movies)} results")
            return movies
            
        except Exception as e:
            print(f"Archive.org search error: {e}")
            return []
    
    
 


    async def _process_search_result(self, doc: dict) -> Optional[dict]:
        """Convert Archive.org document to our movie format with consistent data."""
        
        identifier = doc.get("identifier")
        if not identifier:
            return None
        
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
        
        # Parse runtime from string to seconds
        runtime = None
        runtime_str = doc.get("runtime")
        if runtime_str:
            try:
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
                    # Assume it's already in seconds
                    runtime = int(float(runtime_str))
            except (ValueError, TypeError):
                runtime = None
        
        # Parse rating
        archive_rating = None
        avg_rating = doc.get("avg_rating")
        if avg_rating:
            try:
                archive_rating = float(avg_rating)
            except (ValueError, TypeError):
                archive_rating = None
        
        # Parse downloads
        downloads = doc.get("downloads", 0)
        if isinstance(downloads, list):
            downloads = downloads[0] if downloads else 0
        downloads = int(downloads) if downloads else 0
        
        # Parse genres
        genres = []
        subjects = doc.get("subject", [])
        if isinstance(subjects, str):
            subjects = [subjects]
        
        seen = set()
        for subject in subjects[:5]:
            if isinstance(subject, str):
                genre_name = subject.strip().title()
                if genre_name and genre_name not in seen:
                    genres.append(genre_name)
                    seen.add(genre_name)
        
        # Get torrent URL
        torrent_url = f"{self.BASE_URL}/download/{identifier}/{identifier}_archive.torrent"
        
        return {
            "id": identifier,
            "source": "archive.org",
            "title": doc.get("title", "Unknown"),
            "year": year,
            "runtime": runtime,  # ✅ NOW IN SECONDS, NOT STRING
            "description": doc.get("description", ""),
            "director": doc.get("creator", [None])[0] if doc.get("creator") else None,
            "genres": genres,
            "poster_url": f"{self.BASE_URL}/services/img/{identifier}",
            "archive_rating": archive_rating,
            "downloads": downloads,
            "num_reviews": doc.get("num_reviews", 0),
            "archive_url": f"{self.BASE_URL}/details/{identifier}",
            
            # Basic torrent info for search results
            "torrents": [
                {
                    "quality": "Original",
                    "torrent_url": torrent_url,
                    "magnet_link": None,
                    "seeders": None,
                    "leechers": None,
                    "size_bytes": None,
                    "file_format": "various",
                }
            ],
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
        
            # ====================================================
            # PARSE RUNTIME (Archive.org returns as string)
            # ====================================================
            runtime = None
            runtime_str = metadata.get("runtime")
            if runtime_str:
                try:
                    # Runtime might be "1:32:45" or "5565" (seconds)
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
                    runtime = None
            
            # ====================================================
            # PARSE YEAR (could be string or list)
            # ====================================================
            year = None
            year_str = metadata.get("year")
            if year_str:
                try:
                    if isinstance(year_str, list):
                        year = int(year_str[0])
                    else:
                        year = int(year_str)
                except (ValueError, TypeError):
                    year = None
            
            # ====================================================
            # GET RATING DATA
            # ====================================================
            archive_rating = None
            avg_rating = metadata.get("avg_rating")
            if avg_rating:
                try:
                    archive_rating = float(avg_rating)
                except (ValueError, TypeError):
                    archive_rating = None
            
            # ====================================================
            # GET DOWNLOAD COUNTS
            # ====================================================
            downloads = 0
            downloads_str = metadata.get("downloads")
            if downloads_str:
                try:
                    if isinstance(downloads_str, list):
                        downloads = int(downloads_str[0])
                    else:
                        downloads = int(downloads_str)
                except (ValueError, TypeError):
                    downloads = 0
            
            # ====================================================
            # GET REVIEW COUNT
            # ====================================================
            num_reviews = 0
            reviews_str = metadata.get("num_reviews")
            if reviews_str:
                try:
                    num_reviews = int(reviews_str)
                except (ValueError, TypeError):
                    num_reviews = 0
            
            # ====================================================
            # GET LANGUAGE
            # ====================================================
            language = metadata.get("language")
            if isinstance(language, list):
                language = language[0] if language else None
            
            # ====================================================
            # EXTRACT IMDb ID (if present in metadata)
            # ====================================================
            imdb_id = None
            # Check various possible fields for IMDb ID
            for field in ["identifier", "external-identifier", "imdb"]:
                if field in metadata:
                    value = metadata[field]
                    if isinstance(value, str) and value.startswith("tt"):
                        imdb_id = value
                        break
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str) and item.startswith("tt"):
                                imdb_id = item
                                break
            
            # ====================================================
            # FORMAT GENRES (subjects field in Archive.org)
            # ====================================================
            genres = []
            subjects = metadata.get("subject", [])
            if isinstance(subjects, str):
                subjects = [subjects]
            
            # Clean up genre names (remove duplicates, standardize)
            seen = set()
            for subject in subjects[:10]:  # Limit to 10 genres
                if isinstance(subject, str):
                    # Clean up genre name
                    genre_name = subject.strip().title()
                    if genre_name and genre_name not in seen:
                        genres.append(genre_name)
                        seen.add(genre_name)
            
            # ====================================================
            # FIND VIDEO FILES AND TORRENT INFO
            # ====================================================
            video_files = [
                f for f in files
                if f.get("format") in ["MPEG4", "h.264", "Ogg Video", "Matroska", "MPEG2"]
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
            
            # Create multiple torrent entries for different qualities if available
            for i, video_file in enumerate(video_files[:3]):  # Top 3 qualities
                quality = "Original"
                if len(video_files) > 1:
                    quality = f"{['Best', 'Medium', 'Low'][i] if i < 3 else 'Quality ' + str(i+1)}"
                
                torrents.append({
                    "quality": quality,
                    "torrent_url": torrent_url,
                    "size_bytes": int(video_file.get("size", 0)),
                    "file_format": video_file.get("format"),
                    "filename": video_file.get("name"),
                    "resolution": self._extract_resolution(video_file.get("name", "")),
                    "duration": runtime,  # Same for all qualities
                })
            
            # ====================================================
            # BUILD COMPLETE RESPONSE
            # ====================================================
            return {
                "id": identifier,
                "source": "archive.org",
                "title": metadata.get("title", "Unknown"),
                "year": year,
                "runtime": runtime,
                "description": metadata.get("description", ""),
                "director": metadata.get("director"),
                "language": language,
                "poster_url": f"{self.BASE_URL}/services/img/{identifier}",
                "archive_rating": archive_rating,
                "imdb_id": imdb_id,
                "genres": genres,
                "downloads": downloads,
                "num_reviews": num_reviews,
                "torrents": torrents,
                "archive_url": f"{self.BASE_URL}/details/{identifier}",
                
                # Additional metadata
                "creator": metadata.get("creator"),  # Could be director or production company
                "publisher": metadata.get("publisher"),
                "collection": metadata.get("collection"),
                "date": metadata.get("date"),
                "added_date": metadata.get("addeddate"),
                "publicdate": metadata.get("publicdate"),
                
                # Video file details
                "total_files": len(files),
                "video_files_count": len(video_files),
                "formats_available": list(set(f.get("format") for f in video_files if f.get("format"))),
            }
            
        except Exception as e:
            print(f"Error fetching Archive.org details for {identifier}: {e}")
            return None

    def _extract_resolution(self, filename: str) -> str:
        """Extract resolution from filename."""
        filename_lower = filename.lower()
        
        resolution_patterns = [
            ("4k", "2160p"),
            ("2160p", "2160p"),
            ("1080p", "1080p"),
            ("720p", "720p"),
            ("480p", "480p"),
            ("hd", "720p"),  # Generic HD
            ("sd", "480p"),  # Generic SD
        ]
        for pattern, resolution in resolution_patterns:
            if pattern in filename_lower:
                return resolution
        
        return "Unknown"

    
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