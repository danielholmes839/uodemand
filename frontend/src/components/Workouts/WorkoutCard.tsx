import { Workout } from "client";
import { formatDate, formatTime } from "helper/formatting";
import { Link } from "react-router-dom";

export const Status: React.FC<{ n: number }> = ({ n }) => {
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

type Props = {
  workout: Omit<Workout, "group">;
};

export const WorkoutCard: React.FC<Props> = ({ workout }) => {
  let start = new Date(Date.parse(workout.time));
  let end = new Date(Date.parse(workout.time) + workout.duration * 60000);

  return (
    <div className="px-5 py-3 shadow rounded">
      <h1 className="font-bold tracking-wide">
        {workout.title}{" "}
        <span className="inline float-right">
          <Status n={workout.available} />
        </span>
      </h1>

      <h2 className="font-semibold">{workout.location}</h2>
      <h2 className="mb-1">
        {formatDate(start)} @ {formatTime(start)} - {formatTime(end)}
      </h2>
      <p>
        <Link
          to={`/workout/${workout.barcode}`}
          className="text-blue-500 underline text-sm"
        >
          View {workout.count} data points
        </Link>
        <span className="text-gray-500 text-xs float-right font-normal mt-2">
          ID:{workout.barcode}
        </span>
      </p>
    </div>
  );
};
