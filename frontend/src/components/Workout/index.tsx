import { useWorkoutGroupQuery } from "client";
import { Status } from "components/Workouts/WorkoutCard";
import { formatDate, formatTime } from "helper/formatting";
import { format } from "path";
import { useParams } from "react-router";
import {
  Hint,
  HorizontalGridLines,
  LineMarkSeries,
  LineSeries,
  MarkSeries,
  VerticalGridLines,
  XAxis,
  XYPlot,
  YAxis,
  makeWidthFlexible,
} from "react-vis";

type TimeseriesProps = {
  line: {
    x: number;
    y: number;
  }[];
};

const FlexibleXYPlot = makeWidthFlexible(XYPlot);

const Timeseries: React.FC<TimeseriesProps> = ({ line }) => {
  return (
    <FlexibleXYPlot xType="time" height={300} colorType="linear">
      <HorizontalGridLines />
      <VerticalGridLines />
      <XAxis />
      <YAxis />
      <LineMarkSeries
        data={line}
        sizeRange={[1, 2]}
        lineStyle={{
          opacity: 0.5,
        }}
      />
    </FlexibleXYPlot>
  );
};

export const Workout: React.FC = () => {
  const { barcode } = useParams<{ barcode: string }>();
  const { data } = useWorkoutGroupQuery({
    variables: {
      barcode: parseInt(barcode),
    },
  });

  if (data && data.workout) {
    let line = data.workout.workouts.map((workout) => {
      return {
        x: Date.parse(workout.timestamp),
        y: workout.available,
        size: 1,
      };
    });

    const workout = data.workout.first;
    const start = new Date(Date.parse(workout.time));
    const end = new Date(Date.parse(workout.time) + workout.duration * 60000);

    return (
      <div className="mt-5">
        <h1 className="text-lg font-bold tracking-wide">
          {workout.title} <Status n={data.workout.last.available} />
        </h1>
        <h2 className="font-semibold">{workout.location}</h2>
        <h3>
          {formatDate(start)} @ {formatTime(start)} - {formatTime(end)}
        </h3>
        <Timeseries line={line} />
        <h2 className="font-semibold">Records</h2>
        <p className="my-3">
          {workout.count} records from{"  "}
          {formatDate(new Date(data.workout.first.timestamp))} to{" "}
          {formatDate(new Date(data.workout.last.timestamp))}
        </p>
        <table className="table-auto">
          <thead>
            <td className="p-1 border border-gray-100">Record ID</td>
            <td className="p-1 border border-gray-100">Available</td>
            <td className="p-1 border border-gray-100">Timestamp</td>
          </thead>
          <tbody>
            {data.workout.workouts.map((workout, i) => {
              let css = i % 2 == 0 ? "bg-gray-100" : "";
              return (
                <tr className={css}>
                  <td className="p-1 border border-gray-100">{workout.id}</td>
                  <td className="p-1 border border-gray-100">
                    {workout.available}
                  </td>
                  <td className="p-1 border border-gray-100">
                    {workout.timestamp}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }

  return <></>;
};
