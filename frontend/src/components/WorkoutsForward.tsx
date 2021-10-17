import React from "react";
import { useWorkoutsForwardQuery, Workout } from "client";

function formatDate(date: Date): string {
  return date.toISOString().split("T")[0];
}

function formatTime(date: Date): string {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let meridiem = hours >= 12 ? "pm" : "am";

  hours %= 12;

  if (hours === 0) {
    hours = 12;
  }

  let string = minutes < 10 ? "0" + minutes : minutes;

  return `${hours}:${string}${meridiem}`;
}

const Available: React.FC<{ n: number }> = ({ n }) => {
  return (
    <>
      {n > 0 ? (
        <span className="inline bg-green-500 py-1 px-2 rounded-sm text-white text-xs tracking-wide">
          {n}
        </span>
      ) : (
        <span className="inline bg-red-500 py-1 px-2 rounded-sm text-white text-xs tracking-wide">
          FULL
        </span>
      )}
    </>
  );
};

const update: any = (prev: any, { fetchMoreResult }: any) => {
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

type WorkoutCardProps = {
  workout: Omit<Workout, "group">;
};

const WorkoutCard: React.FC<WorkoutCardProps> = ({ workout }) => {
  let start = new Date(workout.time);
  let end = new Date(workout.time);
  end.setMinutes(end.getMinutes() + workout.duration);

  return (
    <div className="px-5 py-3 shadow mb-3">
      <h1 className="text-xl font-bold">
        {workout.title}{" "}
        <span className="inline float-right">
          <Available n={workout.available} />
        </span>
      </h1>

      <h2 className="font-semibold text-lg">{workout.location}</h2>
      <h2 className="mb-1">
        {formatDate(start)} @ {formatTime(start)} - {formatTime(end)}
      </h2>
      <a className="text-blue-500 underline">
        View {workout.count} data points
      </a>
    </div>
  );
};

export const WorkoutsForward: React.FC = () => {
  const { data, fetchMore } = useWorkoutsForwardQuery({
    variables: {
      first: 10,
    },
  });

  const paginate = (endCursor: string) => {
    fetchMore({
      variables: {
        after: endCursor,
        first: 10,
      },
      updateQuery: update,
    });
  };

  if (data !== undefined && data.workouts) {
    return (
      <>
        <div className="grid grid-cols-3 gap-5 mt-5">
          {data.workouts.edges.map(({ node: workout }) => {
            return <WorkoutCard workout={workout} />;
          })}
        </div>
        <div className="mb-10">
          {data.workouts.pageInfo.hasNextPage && (
            <button
              className="w-full bg-blue-500"
              onClick={() => paginate(data.workouts?.pageInfo.endCursor)}
            >
              More
            </button>
          )}
        </div>
      </>
    );
  } else {
    return <></>;
  }
};
