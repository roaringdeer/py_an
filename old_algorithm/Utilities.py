
def make_unique(lst: list) -> list:
    list_set = set(lst)
    unique_list = (list(list_set))
    return unique_list


def selection_sort(sorter: list, to_sort: list):  # sort list by another, used for sorting chains by preference struct
    for i in range(len(sorter)):
        min_val_i = i
        for j in range(i + 1, len(sorter)):
            if sorter[j] < sorter[min_val_i]:
                min_val_i = j
        sorter[i], sorter[min_val_i] = sorter[min_val_i], sorter[i]
        to_sort[i], to_sort[min_val_i] = to_sort[min_val_i], to_sort[i]
    return to_sort
