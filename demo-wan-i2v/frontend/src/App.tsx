import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';  // Убедитесь, что путь правильный

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />  {/* Главная страница */}
        {/* Добавьте другие маршруты по мере необходимости */}
      </Routes>
    </Router>
  );
}

export default App;
