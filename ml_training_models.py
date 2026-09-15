from ML import (
    get_data_set_data,
    get_data_set_target,
    learn_gradient_boosting_regressor_model,
    learn_linear_regression_model,
    save_model,
)

if __name__ == "__main__":
    features = get_data_set_data()
    target = get_data_set_target()

    linear_model, _, _ = learn_linear_regression_model(features, target)
    save_model(linear_model, "liner_regression.pkl")

    gradient_model, _, _ = learn_gradient_boosting_regressor_model(features, target)
    save_model(gradient_model, "gradient_boosting_regressor.pkl")
