import React, { useEffect, useMemo, useState } from "react";
import { useHistory, useLocation } from "react-router";
import { Tab } from "./tab";
import { WorkoutsForward } from "./WorkoutsFuture";
import { WorkoutsBackward } from "./WorkoutsHistorical";

enum View {
  FUTURE = "future",
  HISTORICAL = "historical",
}

export const Workouts: React.FC = () => {
  const history = useHistory();
  const params = new URLSearchParams(useLocation().search);
  const [view, setView] = useState<View>(
    params.get("view") === "historical" ? View.HISTORICAL : View.FUTURE
  );

  useEffect(() => {
    history.push({
      search: `?view=${view}`,
    });
  }, [view]);

  return (
    <>
      <div className="border-b border-gray-300 mt-3">
        <Tab active={view === View.FUTURE} onClick={() => setView(View.FUTURE)}>
          Future Workouts
        </Tab>
        <Tab
          active={view === View.HISTORICAL}
          onClick={() => setView(View.HISTORICAL)}
        >
          Historical Workouts
        </Tab>
      </div>
      {view === View.FUTURE ? <WorkoutsForward /> : <WorkoutsBackward />}
    </>
  );
};
