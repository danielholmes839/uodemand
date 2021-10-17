type Props = { onClick: () => void; active: boolean };

export const Tab: React.FC<Props> = ({ onClick, active, children }) => {
  let css = active
    ? "font-semibold text-blue-600 py-2 px-3 border-b-2 border-blue-500 text-sm"
    : "font-semibold text-gray-500 py-2 px-3 text-sm";
  return (
    <button onClick={onClick} className={css}>
      {children}
    </button>
  );
};
