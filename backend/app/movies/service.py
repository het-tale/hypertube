from pdb import run
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy import and_, desc, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import db
from app.db.session import get_db
from app.models.movie import Movie
from app.models.comment import Comment
from app.movies.archiveOrg_service import ArchiveOrgService


class MovieService:

    def __init__(self):
        self.archive_service = ArchiveOrgService()

    async def get_movie(self, movie_id: str, db: AsyncSession = Depends(get_db)):
        statement = (
            select(Movie)
            .options(
                selectinload(Movie.cast_members),
                selectinload(Movie.videos),
                selectinload(Movie.comment).selectinload(Comment.user),
            )
            .where(Movie.id == movie_id)
        )
        result = await db.execute(statement)
        movie = result.scalar_one_or_none()
        return movie
    
    async def search_movies(
        self,
        db: AsyncSession,
        query: str,
        page: int = 1,
        limit: int = 20,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Search movies with caching strategy.
        First checks DB cache, then falls back to external API.
        """
        offset = (page - 1) * limit
        
        # Clean query for search
        search_terms = query.lower().strip().split()
        
        # print(f"Searching for '{query}' in cache with terms: {use_cache}")
        if use_cache:
            # Try to find in cache first
            cached_results = await self._search_in_db(db, search_terms, offset, limit)
        
            if len(cached_results) >= limit:
                # We have enough cached results
                for movie in cached_results:
                    movie.increment_search_hits()
                await db.commit()
                # await db.refresh(movie)  # Refresh to ensure we have latest data
                # for movie in cached_results:
                #     await db.refresh(movie, attribute_names=[
                #         'genres',
                #         'cast_members',  # ✅ ADD THIS
                #         'videos',        # ✅ ADD THIS if accessed
                #         'subtitles',     # ✅ ADD THIS if accessed
                #     ])
            

                return {
                    "source": "cache",
                    "query": query,
                    "page": page,
                    "limit": limit,
                    "results": [movie.get_basic_info() for movie in cached_results],
                    "total_in_cache": len(cached_results),
                }
        # Not enough in cache, fetch from Archive.org
        external_results = await self.archive_service.search_movies(query, page, limit)
        # for (external_movie) in external_results:
        #     if external_movie["id"] in [movie.id for movie in cached_results]:
        #         cached_results = [movie for movie in cached_results if movie.id != external_movie["id"]]
        #         print(f"Removed duplicate movie from cache results: {external_movie['id']} - {external_movie['title']}")
        # for movie in cached_results:
        #     print(f"Cached movie: {movie.id} - {movie.title}")
        # print(f"Fetched {len(external_results)} results from Archive.org for '{query}'")
        # Store new results in DB
        stored_movies = []
        for movie_data in external_results:
            movie = await self._create_or_update_movie(db, movie_data, search_query=query, is_basic=True)
            if movie:
                stored_movies.append(movie)
                movie.increment_search_hits()
        
        await db.commit()
        # for movie in stored_movies:
        #     await db.refresh(movie, attribute_names=[
        #         'genres',
        #         'cast_members',  # ✅ ADD THIS
        #         'videos',        # ✅ ADD THIS
        #         'subtitles',     # ✅ ADD THIS
        #     ])
        
        return {
            "source": "external",
            "query": query,
            "page": page,
            "limit": limit,
            "results": [movie.get_basic_info() for movie in stored_movies],
            "total_external": len(external_results),
            "stored_count": len(stored_movies),
        }
    
    async def _search_in_db(
        self,
        db: AsyncSession,
        search_terms: List[str],
        offset: int,
        limit: int
    ) -> List[Movie]:
        """Search movies in database with fuzzy matching."""
        conditions = []
        
        for term in search_terms:
            if len(term) >= 3:  # Only search for meaningful terms
                # Search in title
                conditions.append(Movie.title.ilike(f"%{term}%"))
                # Search in description
                conditions.append(Movie.description.ilike(f"%{term}%"))
                # Search in keywords if available
                conditions.append(Movie.search_keywords.contains([term]))
        
        if not conditions:
            return []
        # print(f"Constructed DB search conditions for terms: {search_terms}")
        # print(f"Conditions s: {conditions}")
        stmt = (
            select(Movie)
            .where(or_(*conditions))
            # .options(selectinload(Movie.genres),
            #          selectinload(Movie.cast_members),  # ✅ ADD THIS
            # selectinload(Movie.videos),  # Add if videos might be accessed
            # selectinload(Movie.subtitles))  # Add if subtitles might be accessed)
            .order_by(desc(Movie.search_cache_hits))
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(stmt)

        # print(f"DB search executed with {len(result.scalars().all())} results")
        return list(result.scalars().all())
    
    async def get_movie_details(
        self,
        db: AsyncSession,
        identifier: str,
        force_refresh: bool = False
    ) -> Optional[Movie]:
        """
        Get full movie details with caching.
        Returns from cache unless stale or forced refresh.
        """
        # First try to get from DB
        stmt = (
            select(Movie)
            .where(Movie.id == identifier)
            .options(
                selectinload(Movie.genres),
                selectinload(Movie.cast_members),
                selectinload(Movie.subtitles)
            )
        )
        
        result = await db.execute(stmt)
        print(f"DB query for movie '{identifier}' executed")
        movie = result.scalar_one_or_none()
        print(f"DB query for movie '{identifier}' executed 222")
        
        should_refresh = (
            force_refresh or
            not movie or
            movie.is_metadata_stale()
        )
        print(f"Should refresh movie '{identifier}': {should_refresh}")
        
        if should_refresh:
            # Fetch fresh data from Archive.org
            external_data = await self.archive_service.get_movie_details(identifier)
            print(f"Fetched details for {identifier} from Archive.org: {len(external_data.keys())} fields")
            if external_data:
                movie = await self._create_or_update_movie(
                    db, external_data, is_basic=False
                )
                if movie:
                    movie.metadata_fetched_at = datetime.utcnow()
                    await db.commit()
        print(f"Returning movie '{identifier}': {movie is not None}")
        return movie
    
    async def _create_or_update_movie(
        self,
        db: AsyncSession,
        movie_data: Dict[str, Any],
        search_query: Optional[str] = None,
        is_basic: bool = True
        
    ) -> Optional[Movie]:
        """Create or update a movie in the database."""

        # print("Creating or updating movie:", movie_data)
        # print("Creating or updating movie check:", movie_data.get('id'))
        if not movie_data or 'id' not in movie_data:
            return None
        
        # Check if movie already exists
        stmt = select(Movie).where(Movie.id == movie_data['id'])
        result = await db.execute(stmt)
        existing_movie = result.scalar_one_or_none()
        # print(f"Existing movie found: {existing_movie is not None}")
        if existing_movie:
            # Update existing movie
            return await self._update_movie(existing_movie, movie_data, is_basic, search_query=search_query)
        else:
            # Create new movie
            return await self._create_movie(db, movie_data, is_basic, search_query=search_query)
    
    async def _create_movie(
        self,
        db: AsyncSession,
        movie_data: Dict[str, Any],
        is_basic: bool,
        search_query: Optional[str] = None
    ) -> Movie:
        """Create a new movie record."""


         # Ensure runtime is integer (seconds)
        runtime = movie_data.get('runtime')
        if runtime is not None:
            try:
                # Convert to int if it's not already
                if not isinstance(runtime, int):
                    # If it's a string like "18:31", parse it
                    if isinstance(runtime, str) and ":" in runtime:
                        parts = runtime.split(":")
                        if len(parts) == 3:
                            h, m, s = parts
                            runtime = int(h) * 3600 + int(m) * 60 + int(s)
                        elif len(parts) == 2:
                            m, s = parts
                            runtime = int(m) * 60 + int(s)
                        else:
                            runtime = int(float(runtime))
                    else:
                        runtime = int(float(runtime))
            except (ValueError, TypeError):
                runtime = None

        movie = Movie(
            id=movie_data['id'],
            source=movie_data.get('source', 'archive.org'),
            title=movie_data.get('title', 'Unknown'),
            description=movie_data.get('description'),
            year=movie_data.get('year'),
            runtime=runtime,
            director=movie_data.get('director'),
            language=movie_data.get('language'),
            poster_url=movie_data.get('poster_url'),
            archive_rating=movie_data.get('rating'),
            archive_url=movie_data.get('archive_url'),
            downloads=movie_data.get('downloads', 0),
            num_reviews=movie_data.get('num_reviews', 0),
            torrents=movie_data.get('torrents'),
            search_keywords=self._extract_keywords(movie_data, search_query=search_query),
            metadata_fetched_at=datetime.utcnow() if not is_basic else None,
        )
        
        movie.update_popularity_score()
        db.add(movie)
        await db.flush()  # Get ID for relationships if needed
        
        return movie
    
    async def _update_movie(
        self,
        movie: Movie,
        movie_data: Dict[str, Any],
        is_basic: bool,
        search_query: Optional[str] = None
    ) -> Movie:
        """Update an existing movie record."""
        # Only update basic fields if we have basic data
        # or if we don't have full metadata yet
        if is_basic and movie.metadata_fetched_at:
            # Don't overwrite full metadata with basic info
            return movie
        

         # Parse runtime if provided
        if 'runtime' in movie_data:
            runtime = movie_data.get('runtime')
            if runtime is not None:
                try:
                    if not isinstance(runtime, int):
                        if isinstance(runtime, str) and ":" in runtime:
                            parts = runtime.split(":")
                            if len(parts) == 3:
                                h, m, s = parts
                                runtime = int(h) * 3600 + int(m) * 60 + int(s)
                            elif len(parts) == 2:
                                m, s = parts
                                runtime = int(m) * 60 + int(s)
                            else:
                                runtime = int(float(runtime))
                        else:
                            runtime = int(float(runtime))
                except (ValueError, TypeError):
                    runtime = None

        movie.runtime = runtime
        # Update fields
        movie.title = movie_data.get('title', movie.title)
        movie.description = movie_data.get('description', movie.description)
        movie.year = movie_data.get('year', movie.year)
        movie.runtime = runtime
        movie.director = movie_data.get('director', movie.director)
        movie.language = movie_data.get('language', movie.language)
        movie.poster_url = movie_data.get('poster_url', movie.poster_url)
        movie.archive_rating = movie_data.get('rating', movie.archive_rating)
        movie.downloads = movie_data.get('downloads', movie.downloads)
        movie.num_reviews = movie_data.get('num_reviews', movie.num_reviews)
        movie.torrents = movie_data.get('torrents', movie.torrents)
        movie.search_keywords = self._extract_keywords(movie_data, search_query=search_query)
        if not is_basic:
            movie.metadata_fetched_at = datetime.utcnow()
        
        movie.update_popularity_score()
        
        return movie
    
    def _extract_keywords(self, movie_data: Dict[str, Any], search_query: Optional[str] = None) -> List[str]:
        """Extract search keywords from movie data, optionally including search context."""
        keywords = set()
        
        # Add title words
        if 'title' in movie_data:
            keywords.update(movie_data['title'].lower().split())
        
        # Add director name parts
        if 'director' in movie_data and movie_data['director']:
            keywords.update(movie_data['director'].lower().split())
        
        # Add year
        if 'year' in movie_data and movie_data['year']:
            keywords.add(str(movie_data['year']))
        
        # Add first 5 genres
        if 'genres' in movie_data:
            for genre in movie_data['genres'][:5]:
                keywords.add(genre.lower())
        
        # ✅ CRITICAL: Add search query that found this movie
        if search_query:
            # Clean and add individual words from query
            query_terms = search_query.lower().strip().split()
            keywords.update(query_terms)
    
        return list(keywords)
    
    async def fetch_and_store_popular_movies(
        self,
        db: AsyncSession,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Fetch popular movies from Archive.org and store in DB.
        This should be called by a cron job.
        """
        # logger.info(f"Fetching {limit} popular movies from Archive.org")
        
        # First, clear previous popular flags
        await db.execute(
            update(Movie)
            .where(Movie.is_popular == True)
            .values(is_popular=False, popularity_rank=None)
        )
        
        # Fetch popular movies (using empty query to get trending)
        popular_data = await self.archive_service.search_movies(
            query="",  # Empty query might return popular
            page=1,
            limit=limit
        )
        
        stored_count = 0
        for rank, movie_data in enumerate(popular_data, 1):
            movie = await self._create_or_update_movie(db, movie_data, is_basic=True)
            if movie:
                movie.is_popular = True
                movie.popularity_rank = rank
                movie.update_popularity_score()
                stored_count += 1
        
        await db.commit()
        
        # logger.info(f"Stored {stored_count} popular movies")
        
        return {
            "fetched": len(popular_data),
            "stored": stored_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_popular_movies(
        self,
        db: AsyncSession,
        limit: int = 20,
        offset: int = 0
    ) -> List[Movie]:
        """Get popular movies from database."""
        stmt = (
            select(Movie)
            .where(Movie.is_popular == True)
            .options(selectinload(Movie.genres))
            .order_by(Movie.popularity_rank)
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def cleanup_stale_cache(
        self,
        db: AsyncSession,
        days_threshold: int = 90
    ) -> Dict[str, Any]:
        """
        Clean up old cached movies that haven't been accessed.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_threshold)
        
        # Find movies to clean up (not downloaded, not watched recently, not popular)
        stmt = (
            select(Movie)
            .where(
                and_(
                    Movie.downloaded == False,
                    Movie.is_popular == False,
                    or_(
                        Movie.last_searched_at < cutoff_date,
                        Movie.last_searched_at.is_(None)
                    ),
                    or_(
                        Movie.last_watched_at < cutoff_date,
                        Movie.last_watched_at.is_(None)
                    )
                )
            )
        )
        
        result = await db.execute(stmt)
        movies_to_delete = list(result.scalars().all())
        
        deleted_count = 0
        for movie in movies_to_delete:
            await db.delete(movie)
            deleted_count += 1
        
        await db.commit()
        
        return {
            "deleted_count": deleted_count,
            "threshold_days": days_threshold,
            "timestamp": datetime.utcnow().isoformat()
        }


# Singleton instance



movie_service = MovieService()
