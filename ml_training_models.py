from ML import (
    get_data_set_data,
    get_data_set_target,
    learn_gradient_boosting_regressor_model,
    learn_linear_regression_model,
    save_model,
)

if __name__ == "__main__":
    model = learn_linear_regression_model(get_data_set_data(), get_data_set_target())
    save_model(model, "liner_regression.pkl")
    learn_gradient_boosting_regressor_model(get_data_set_data(), get_data_set_target())
    save_model(model, "gradient_boosting_regressor.pkl")
