import React, { useState } from "react";
import { PredictionRequest, PredictionResponse } from "../types/predict";
import { predict, sendFeedback } from "../api/predictApi";

const initialForm: PredictionRequest = {
  MedInc: 8.3252,
  HouseAge: 41,
  AveRooms: 6.984127,
  AveBedrms: 1.02381,
  Population: 322,
  AveOccup: 2.264706,
  Latitude: 37.88,
  Longitude: -122.23,
};
const fields: { key: keyof PredictionRequest; label: string; hint: string }[] = [
  { key: "MedInc", label: "Средний доход", hint: "в десятках тысяч USD" },
  { key: "HouseAge", label: "Возраст дома", hint: "лет" },
  { key: "AveRooms", label: "Среднее число комнат", hint: "на домохозяйство" },
  { key: "AveBedrms", label: "Среднее число спален", hint: "на домохозяйство" },
  { key: "Population", label: "Население района", hint: "человек" },
  { key: "AveOccup", label: "Средняя заселённость", hint: "человек на дом" },
  { key: "Latitude", label: "Широта", hint: "координата" },
  { key: "Longitude", label: "Долгота", hint: "координата" },
];

const PredictPage: React.FC = () => {
  const [form, setForm] = useState(initialForm);
  const [modelName, setModelName] = useState("linear_regression");
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [feedbackSent, setFeedbackSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    setForm({ ...form, [event.target.name]: Number(event.target.value) });
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setFeedbackSent(false);
    try {
      setResult(await predict(modelName, form));
    } catch (error: any) {
      setResult({
        status: "error",
        message: error?.response?.data?.detail || "Не удалось получить прогноз.",
        prediction: null,
      });
    } finally {
      setLoading(false);
    }
  };
  const handleFeedback = async (isCorrect: boolean) => {
    if (!result?.prediction) return;
    try {
      await sendFeedback({
        ...form,
        modelName,
        prediction: result.prediction / 100_000,
        isCorrect,
      });
      setFeedbackSent(true);
    } catch {
      setResult({ ...result, message: "Прогноз получен, но отзыв сохранить не удалось." });
    }
  };
  return (
    <div className="page-grid page-grid--predict">
      <section className="page-heading">
        <span className="eyebrow">Prediction studio</span>
        <h1>Оцените стоимость жилья</h1>
        <p>Заполните характеристики объекта — модель вернёт оценку стоимости в долларах США.</p>
      </section>
      <div className="content-grid">
        <form className="card prediction-form" onSubmit={handleSubmit}>
          <div className="form-section">
            <label className="field-label" htmlFor="model">
              Модель для расчёта
            </label>
            <select
              id="model"
              value={modelName}
              onChange={(event) => setModelName(event.target.value)}
            >
              <option value="linear_regression">Линейная регрессия</option>
              <option value="gradient_boosting_regressor">Градиентный бустинг</option>
            </select>
          </div>
          <div className="form-divider">
            <span>Параметры объекта</span>
          </div>
          <div className="field-grid">
            {fields.map(({ key, label, hint }) => (
              <label className="field" key={key}>
                <span>{label}</span>
                <input
                  type="number"
                  name={key}
                  value={form[key]}
                  step="any"
                  onChange={handleChange}
                  required
                />
                <small>{hint}</small>
              </label>
            ))}
          </div>
          <button className="button button--primary button--wide" type="submit" disabled={loading}>
            {loading ? "Рассчитываем…" : "Получить прогноз"} <span>→</span>
          </button>
        </form>
        <aside className="result-column">
          <div className="model-note">
            <span className="model-note__icon">✦</span>
            <div>
              <strong>Как это работает</strong>
              <p>
                Модель учитывает доход, параметры дома, плотность населения и геолокацию района.
              </p>
            </div>
          </div>
          {result ? (
            <div className={`result-card result-card--${result.status}`}>
              <span className="result-card__label">
                {result.status === "success" ? "Оценка стоимости" : "Ошибка расчёта"}
              </span>
              {result.prediction !== null && (
                <strong className="result-card__value">
                  ${result.prediction.toLocaleString("ru-RU", { maximumFractionDigits: 0 })}
                </strong>
              )}
              <p>{result.message}</p>
              {result.prediction !== null && (
                <div className="feedback">
                  <span>Прогноз оказался полезным?</span>
                  <div>
                    <button disabled={feedbackSent} onClick={() => handleFeedback(true)}>
                      Да
                    </button>
                    <button disabled={feedbackSent} onClick={() => handleFeedback(false)}>
                      Не совсем
                    </button>
                  </div>
                  {feedbackSent && <small>Спасибо, отзыв сохранён.</small>}
                </div>
              )}
            </div>
          ) : (
            <div className="empty-result">
              <span>⌁</span>
              <strong>Результат появится здесь</strong>
              <p>Выберите модель и заполните параметры слева.</p>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
};
export default PredictPage;
