export default function FilterButton({ filter, selected, onClick }) {
  return (
    <div
      className={`flex flex-col items-center justify-center min-w-[80px] h-24 p-2 rounded-xl border 
        ${selected ? 'bg-white/30 border-white' : 'bg-white/10 border-white/20'} 
        cursor-pointer transition hover:bg-white/20`}
      onClick={onClick}
    >
      <img src={filter.icon} alt={filter.name} className="w-10 h-10 object-contain mb-1" />
      <span className="text-xs font-semibold">{filter.name}</span>
    </div>
  );
}
