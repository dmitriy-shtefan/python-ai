from random import Random

from torch.utils.data import Subset


def balanced_subset_indices(targets, per_class, seed=42):
    rng = Random(seed)
    by_class = {}

    for idx, label in enumerate(targets):
        by_class.setdefault(int(label), []).append(idx)

    selected = []
    for label in sorted(by_class):
        indices = by_class[label]
        rng.shuffle(indices)
        selected.extend(indices[:per_class])

    rng.shuffle(selected)
    return selected


def make_balanced_subset(dataset, per_class, seed=42):
    return Subset(
        dataset,
        balanced_subset_indices(dataset.targets, per_class=per_class, seed=seed),
    )


def make_cifar10_demo_subsets(train_dataset, test_dataset, seed=42):
    return (
        make_balanced_subset(train_dataset, per_class=200, seed=seed),
        make_balanced_subset(test_dataset, per_class=50, seed=seed),
    )


def make_resnet_demo_subsets(train_dataset, test_dataset, seed=42):
    return (
        make_balanced_subset(train_dataset, per_class=20, seed=seed),
        make_balanced_subset(test_dataset, per_class=10, seed=seed),
    )
