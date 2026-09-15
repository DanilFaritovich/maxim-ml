import React from "react";
import { BrowserRouter as Router, NavLink, Route, Routes } from "react-router-dom";

import "./App.css";
import PredictPage from "./pages/PredictPage";
import TrainModelPage from "./pages/TrainModelPage";

function WelcomePage() {
  return (
    <section className="hero">
      <div className="hero__eyebrow">Machine learning workspace</div>
      <h1>
        Оценка стоимости жилья
        <br />
        на основе данных
      </h1>
      <p className="hero__copy">
        Обучайте регрессионные модели, получайте прогнозы и отслеживайте качество последних запусков
        в одном интерфейсе.
      </p>
      <div className="hero__actions">
        <NavLink className="button button--primary" to="/predict">
          Сделать прогноз <span>→</span>
        </NavLink>
        <NavLink className="button button--secondary" to="/train">
          Обучить модель
        </NavLink>
      </div>
      <div className="hero__metrics">
        <div>
          <strong>2</strong>
          <span>регрессионные модели</span>
        </div>
        <div>
          <strong>8</strong>
          <span>характеристик жилья</span>
        </div>
        <div>
          <strong>API</strong>
          <span>FastAPI + React</span>
        </div>
      </div>
    </section>
  );
}

function App() {
  return (
    <Router>
      <div className="app-shell">
        <header className="topbar">
          <NavLink className="brand" to="/">
            <span className="brand__mark">M</span>
            <span>
              Maxim<span>ML</span>
            </span>
          </NavLink>
          <nav aria-label="Основная навигация" className="navigation">
            <NavLink end to="/">
              Обзор
            </NavLink>
            <NavLink to="/predict">Прогноз</NavLink>
            <NavLink to="/train">Обучение</NavLink>
          </nav>
          <a className="docs-link" href="/docs" target="_blank" rel="noreferrer">
            API Docs ↗
          </a>
        </header>
        <main className="page-container">
          <Routes>
            <Route path="/" element={<WelcomePage />} />
            <Route path="/train" element={<TrainModelPage />} />
            <Route path="/predict" element={<PredictPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
