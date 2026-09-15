import axios from "axios";
import { TrainHistoryItem } from "../types/train";

export const trainModel = async (modelName: string) => {
  const response = await axios.post(`/train/${modelName}`);
  return response.data;
};

export const getTrainHistory = async (): Promise<TrainHistoryItem[]> => {
  const response = await axios.get(`/train/history`);
  return response.data;
};
