'use client'

import { useEffect, useState } from 'react';

const MovieList = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const res = await fetch('http://localhost:8000/movie/');
        
        // Check if the response is okay (status code 200-299)
        if (!res.ok) {
          throw new Error(`Error: ${res.status} - ${res.statusText}`);
        }

        const data = await res.json();
        console.log(data); // For debugging purposes
        setMovies(data);
      } catch (error) {
        console.error("Failed to fetch movies:", error.message);
        // You can also use this error to display a message to users if needed
      }
    };

    fetchMovies();
  }, []);

  return (
    <div>
      <h1>Movie List</h1>
      <ul>
        {movies.map((movie, index) => (
          <li key={index}>{movie.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default MovieList;
