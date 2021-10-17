import { useWorkoutsForwardQuery } from "client";
import { ErrorAlert } from "components/Error";
import { Loading } from "components/Loading";
import { update } from "helper/update";
import { WorkoutCard } from "./WorkoutCard";

export const WorkoutsForward: React.FC = () => {
  const { data, loading, error, fetchMore } = useWorkoutsForwardQuery({
    variables: {
      first: 12,
    },
  });

  const paginate = (endCursor: string) => {
    fetchMore({
      variables: {
        after: endCursor,
        first: 12,
      },
      updateQuery: update,
    });
  };

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorAlert category={"Server"} message={error.message} />;
  }

  if (data && data.workouts === undefined) {
    return <ErrorAlert category="User" message="Invalid cursor" />;
  }

  if (data && data.workouts) {
    return (
      <>
        <div className="grid lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-5 mt-5">
          {data.workouts.edges.map(({ node: workout }) => {
            return <WorkoutCard key={workout.id} workout={workout} />;
          })}
        </div>
        <div className="mb-10 mt-5">
          {data.workouts.pageInfo.hasNextPage && (
            <button
              className="bg-gray-50 py-3 text-sm px-10 rounded font-semibold text-gray-900"
              onClick={() => paginate(data.workouts?.pageInfo.endCursor)}
            >
              Load More
            </button>
          )}
        </div>
      </>
    );
  } else {
    return <></>;
  }
};
