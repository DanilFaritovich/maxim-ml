import { render, screen } from "@testing-library/react";

import PredictPage from "./PredictPage";

jest.mock("../api/predictApi", () => ({
  predict: jest.fn(),
  sendFeedback: jest.fn(),
}));

describe("PredictPage", () => {
  it("renders the prediction form with a default model", () => {
    render(<PredictPage />);

    expect(screen.getByRole("heading", { name: /оцените стоимость жилья/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/модель для расчёта/i)).toHaveValue("linear_regression");
    expect(screen.getByRole("button", { name: /получить прогноз/i })).toBeInTheDocument();
  });
});
