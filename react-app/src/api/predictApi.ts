import axios from "axios";
import { PredictionRequest, PredictionResponse, FeedbackData } from "../types/predict";

export const predict = async (
  modelName: string,
  data: PredictionRequest,
): Promise<PredictionResponse> => {
  const response = await axios.post<PredictionResponse>(`/predict/${modelName}`, data);
  return response.data;
};

export const sendFeedback = async (feedback: FeedbackData): Promise<void> => {
  await axios.post("/train_feedback/feedback", feedback);
};
