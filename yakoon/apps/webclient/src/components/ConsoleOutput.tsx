type Props = {
  lines: string[];
};

export function ConsoleOutput({ lines }: Props) {
  return (
    <div className="bg-black text-green-400 font-mono p-4 h-96 overflow-y-auto rounded">
      {lines.map((line, i) => (
        <div key={i}>{line}</div>
      ))}
    </div>
  );
}
