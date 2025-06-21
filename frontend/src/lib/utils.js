// Simple clsx replacement
function clsx(...classes) {
  return classes
    .filter(Boolean)
    .map(cls => typeof cls === 'string' ? cls : '')
    .join(' ');
}

// Simple tailwind-merge replacement (just return combined classes)
function twMerge(...classes) {
  return clsx(...classes);
}

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
