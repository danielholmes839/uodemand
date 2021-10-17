type Props = {
  category: string;
  message: string;
};

export const ErrorAlert: React.FC<Props> = ({ message, category }) => {
  return (
    <div className="bg-red-200 p-3 mt-3 rounded text-red-800">
      <h1>
        {category} Error: {message}
      </h1>
    </div>
  );
};
