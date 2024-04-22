import React from 'react';
import './App.css';

interface AppProps {
  // define props here
}

const App: React.FC<AppProps> = (props) => {
  return (
    <div className="App">
      <header className="App-header">
          <h1>Guess the player by 2K Rating</h1>
      </header>
    </div>
  );
}

export default App;
