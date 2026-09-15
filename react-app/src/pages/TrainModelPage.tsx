import React, { useEffect, useState } from "react";
import { getTrainHistory, trainModel } from "../api/trainApi";
import { ModelName, TrainHistoryItem, TrainResponse } from "../types/train";

const modelOptions: { label: string; value: ModelName; description: string }[] = [
  {
    label: "Linear Regression",
    value: "linear_regression",
    description: "Быстрый и интерпретируемый базовый прогноз.",
  },
  {
    label: "Gradient Boosting",
    value: "gradient_boosting_regressor",
    description: "Более точная модель для сложных зависимостей.",
  },
];

const TrainModelPage: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState<ModelName>("linear_regression");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<TrainResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<TrainHistoryItem[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const selected = modelOptions.find((model) => model.value === selectedModel)!;
  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      setHistory(await getTrainHistory());
    } finally {
      setHistoryLoading(false);
    }
  };
  useEffect(() => {
    fetchHistory();
  }, []);
  const handleTrain = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      setResponse(await trainModel(selectedModel));
      await fetchHistory();
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Не удалось завершить обучение. Проверьте подключение к серверу.",
      );
      await fetchHistory();
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="page-grid">
      <section className="page-heading">
        <span className="eyebrow">Training centre</span>
        <h1>Переобучите модель</h1>
        <p>
          Запустите новую тренировку на California Housing и сохраните результат для следующих
          прогнозов.
        </p>
      </section>
      <div className="training-layout">
        <section className="card training-card">
          <div className="card-heading">
            <div>
              <h2>Настройка запуска</h2>
              <p>Выберите алгоритм для обучения.</p>
            </div>
            <span className="status-dot">Готово</span>
          </div>
          <div className="model-options">
            {modelOptions.map((model) => (
              <label
                className={`model-option ${selectedModel === model.value ? "model-option--selected" : ""}`}
                key={model.value}
              >
                <input
                  type="radio"
                  name="model"
                  value={model.value}
                  checked={selectedModel === model.value}
                  onChange={() => setSelectedModel(model.value)}
                />
                <span className="model-option__radio" />
                <span>
                  <strong>{model.label}</strong>
                  <small>{model.description}</small>
                </span>
              </label>
            ))}
          </div>
          <div className="training-info">
            <span>⌛</span>
            <p>
              {selectedModel === "gradient_boosting_regressor"
                ? "Градиентный бустинг может обучаться несколько минут."
                : "Линейная регрессия обычно обучается быстро."}
            </p>
          </div>
          <button
            className="button button--primary button--wide"
            onClick={handleTrain}
            disabled={loading}
          >
            {loading ? "Идёт обучение модели…" : `Обучить ${selected.label}`} <span>→</span>
          </button>
          {response && (
            <div className="notice notice--success">
              <strong>Обучение завершено</strong>
              <span>{response.message}</span>
            </div>
          )}
          {error && (
            <div className="notice notice--error">
              <strong>Не удалось завершить обучение</strong>
              <span>{error}</span>
            </div>
          )}
        </section>
        <aside className="training-aside">
          <div className="stat-card">
            <span>Модели</span>
            <strong>2</strong>
            <p>Linear Regression и Gradient Boosting</p>
          </div>
          <div className="stat-card">
            <span>Датасет</span>
            <strong>20 640</strong>
            <p>наблюдений California Housing</p>
          </div>
          <div className="stat-card stat-card--accent">
            <span>Совет</span>
            <p>
              После обучения перейдите в «Прогноз», чтобы сравнить результат обновлённой модели.
            </p>
          </div>
        </aside>
      </div>
      <section className="history-section">
        <div className="history-section__heading">
          <div>
            <span className="eyebrow">Recent runs</span>
            <h2>История обучения</h2>
          </div>
          <button className="text-button" onClick={fetchHistory} disabled={historyLoading}>
            Обновить ↻
          </button>
        </div>
        {historyLoading ? (
          <div className="history-placeholder">Загружаем историю…</div>
        ) : history.length === 0 ? (
          <div className="history-placeholder">Запусков пока нет.</div>
        ) : (
          <div className="history-table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Дата</th>
                  <th>Модель</th>
                  <th>Статус</th>
                  <th>R²</th>
                  <th>MSE</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>{new Date(item.timestamp).toLocaleString()}</td>
                    <td>
                      {item.model_name === "linear_regression"
                        ? "Linear Regression"
                        : "Gradient Boosting"}
                    </td>
                    <td>
                      <span className={`badge badge--${item.status}`}>
                        {item.status === "success" ? "Успешно" : "Ошибка"}
                      </span>
                    </td>
                    <td>{item.R2.toFixed(3)}</td>
                    <td>{item.MSE.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};
export default TrainModelPage;
