from AnticipatoryNetwork import AnticipatoryNetwork
import ExcelReader as exr
import TextWriter as txw


def go():
    try:
        decisions, criterias, feedbacks, coefficients = exr.go()
        an = AnticipatoryNetwork(decisions, criterias, feedbacks, coefficients)
        # an.print()
        all_paths = an.get_all_paths()
        optimal_chains_for_paths = []
        for path in all_paths:
            admissible_chains = an.get_admissible_chains(path)
            optimal_chains_for_path = an.get_optimal_chains_for_path(path, admissible_chains)
            optimal_chains_for_paths.append(optimal_chains_for_path)
        optimal_chains_for_tree = an.get_optimal_chains_for_tree(optimal_chains_for_paths)
        best_optimal_chain, best_optimal_chain_cost = an.find_best_optimal(optimal_chains_for_tree)
    except BaseException as e:
        print("Failed algorithm: {}".format(str(e)))
        return None
    else:
        print(an.log)
        txw.go(an.log)
        return optimal_chains_for_tree, best_optimal_chain
