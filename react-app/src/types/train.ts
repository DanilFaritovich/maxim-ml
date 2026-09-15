export type ModelName = "linear_regression" | "gradient_boosting_regressor";

export interface TrainResponse {
  status: string;
  message: string;
  model_name?: string | null;
}

export interface TrainHistoryItem {
  id: number;
  model_name: string;
  status: string;
  message: string;
  R2: number;
  MSE: number;
  timestamp: string; // ISO string
}
