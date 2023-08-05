import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Content() {
  // Use React's useState hook to create a state variable to hold your data
  const [articles, setArticles] = useState([]);

  // Use the useEffect hook to fetch data when the component mounts
  useEffect(() => {
    // Define the async function that fetches data
    const fetchData = async () => {
      try {
        // Make a GET request to your API endpoint
        const response = await axios.get('http://localhost:8000/api/articles');
        
        // Update the state variable with the data from the server
        setArticles(response.data);
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    // Call the fetch function
    fetchData();
  }, []);  // The empty array means this effect runs once when the component mounts

  // Render the fetched data
  return (
    <div className="Content">
      {articles.map((article, index) => (
        <div key={index}>
          <h2>{article.title}</h2>
          <p>{article.summary}</p>
          <p>Stock Tickers: {article.stock_tickers.join(", ")}</p>
          <p>Sentiment: {article.sentiment}</p>
          <p>Reasoning: {article.reasoning}</p>
        </div>
      ))}
    </div>
  );
}

export default Content;
