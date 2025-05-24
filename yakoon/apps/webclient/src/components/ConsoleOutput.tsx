type Props = {
  lines: string[];
};

export function ConsoleOutput({ lines }: Props) {
  return (
    <div className="h-full border border-zinc-700 rounded-md p-4 bg-zinc-800 text-gray-100 font-mono space-y-1">
      {lines.map((line, i) => (
        <div key={i}>{line}</div>
      ))}
    </div>
  );
}
