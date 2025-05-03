import { useState, useEffect } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [portfolioData, setPortfolioData] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      const response = await fetch('http://localhost:8000/portfolio/data');
      const data = await response.json();
      setPortfolioData(data.portfolio);
    } catch (error) {
      console.error('Error fetching portfolio data:', error);
    }
  };

  const handleStockSelection = (stock) => {
    setSelectedStock(stock);
    fetchGraphData(stock);
  };

  const fetchGraphData = async (stock) => {
    try {
      const response = await fetch(`http://localhost:8000/portfolio/graph?stock=${stock}`);
      const data = await response.json();
      setGraphData(data);
    } catch (error) {
      console.error('Error fetching graph data:', error);
    }
  };

  const handleAddStock = async (stock) => {
    try {
      const response = await fetch('http://localhost:8000/portfolio/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock }),
      });
      if (response.ok) {
        fetchPortfolioData();
      } else {
        console.error('Error adding stock:', response.statusText);
      }
    } catch (error) {
      console.error('Error adding stock:', error);
    }
  };

  const handleRemoveStock = async (stock) => {
    try {
      const response = await fetch('http://localhost:8000/portfolio/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock }),
      });
      if (response.ok) {
        fetchPortfolioData();
      } else {
        console.error('Error removing stock:', response.statusText);
      }
    } catch (error) {
      console.error('Error removing stock:', error);
    }
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <div className="portfolio">
        <h2>Portfolio</h2>
        <ul>
          {portfolioData.map((stock) => (
            <li key={stock} onClick={() => handleStockSelection(stock)}>
              {stock}
              <button onClick={() => handleRemoveStock(stock)}>Remove</button>
            </li>
          ))}
        </ul>
        <input
          type="text"
          placeholder="Add stock"
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleAddStock(e.target.value);
              e.target.value = '';
            }
          }}
        />
      </div>
      <div className="graph">
        <h2>Graph</h2>
        {graphData ? (
          <img src={`data:image/png;base64,${graphData}`} alt="Stock Graph" />
        ) : (
          <p>Select a stock to view the graph</p>
        )}
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
