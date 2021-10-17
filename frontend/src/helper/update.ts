export const update: any = (prev: any, { fetchMoreResult }: any) => {
  if (
    !fetchMoreResult ||
    !fetchMoreResult.workouts ||
    !prev ||
    !prev.workouts
  ) {
    return undefined;
  }

  fetchMoreResult.workouts.edges = [
    ...prev.workouts.edges,
    ...fetchMoreResult.workouts.edges,
  ];

  return fetchMoreResult;
};
