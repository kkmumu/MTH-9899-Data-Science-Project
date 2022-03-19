## Author: Shangwen Sun

from prep import *


def regmodel_hyperparameter_tuning(alphas_to_try, X, y, n_splits = 5, how_cv = "walk_forwarding", scoring = "weighted_r2", model_name = 'Ridge', X_test = None, y_test = None, draw_plot = False, filename = None):
    
    # tuning the hyper-parameter by grid searching
    # optimising on one basis but then comparing performance on another
    # scoring method: weighted R-squared
    
    validation_scores = []
    train_scores = []
    results_list = []
    
    if X_test is not None:
        test_scores = []
    else:
        test_scores = None

    for curr_alpha in alphas_to_try:
        if model_name == 'Lasso':
            regmodel = Lasso(alpha = curr_alpha, tol = 1e-15)
            
        elif model_name == 'Ridge':
            regmodel = Ridge(alpha = curr_alpha)
            
        elif model_name == 'SimpleLR':
            regmodel = LinearRegression()
            
        else:
            return None

        results = self_cross_validation(regmodel, X, y, n_splits = n_splits, how = how_cv)
        #tscv = TimeSeriesSplit(n_splits = n_splits)
        #results = cross_validate(regmodel, X, y, scoring = "r2", cv=tscv, return_train_score = True)
        validation_scores.append(np.mean(results['test_score']))
        train_scores.append(np.mean(results['train_score']))
        results_list.append(results)
        print(results)

        if X_test is not None:
            regmodel = regmodel.fit(X, y)
            y_pred = regmodel.predict(X_test)
            r2_weight = 1 / X_test["estVol winsorized"]
            #test_scores.append(weighted_r2_scorer(regmodel, X_test, y_test)) #######################
            test_scores.append(r2_score(y_test, y_pred, sample_weight = r2_weight))

    chosen_alpha_id = np.argmax(validation_scores)
    chosen_alpha = alphas_to_try[chosen_alpha_id]
    max_validation_score = np.max(validation_scores)
    
    if X_test is not None:
        test_score_at_chosen_alpha = test_scores[chosen_alpha_id]
    else:
        test_score_at_chosen_alpha = None
        
    if draw_plot:
        regmodel_param_plot(validation_scores, train_scores, alphas_to_try, chosen_alpha,
                            model_name, scoring, test_scores, filename)
        
    print("Chosen alpha: %.5f" % chosen_alpha)
    print("Validation score: %.5f" % max_validation_score)
    print("Test score at chosen alpha: %.5f" % test_score_at_chosen_alpha)
    
    return chosen_alpha, max_validation_score, test_score_at_chosen_alpha




def regmodel_param_plot(validation_score, train_score, alphas_to_try, chosen_alpha, scoring, model_name, test_score = None, filename = None):
    
    plt.figure(figsize = (8,8))
    sns.lineplot(y = validation_score, x = alphas_to_try, label = 'validation_data')
    sns.lineplot(y = train_score, x = alphas_to_try, label = 'training_data')
    plt.axvline(x = chosen_alpha, linestyle = '--')
    
    if test_score is not None:
        sns.lineplot(y = test_score, x = alphas_to_try, label = 'test_data')
        
    plt.xlabel('alpha_parameter')
    plt.ylabel(scoring)
    plt.title(model_name + ' Regularization')
    plt.legend()
    
    if filename is not None:
        plt.savefig(str(filename) + ".png")
        
    plt.show()
    


