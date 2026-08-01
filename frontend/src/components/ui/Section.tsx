import type { ReactNode } from 'react';

interface SectionProps {
  id?: string;
  children: ReactNode;
  className?: string;
  size?: 'sm' | 'md';
}

export function Section({ id, children, className = '', size = 'md' }: SectionProps) {
  return (
    <section id={id} className={`container-dbn ${size === 'sm' ? 'section-sm' : 'section'} ${className}`.trim()}>
      {children}
    </section>
  );
}

interface SectionHeadingProps {
  eyebrow?: string;
  title: ReactNode;
  description?: ReactNode;
  align?: 'center' | 'left';
  className?: string;
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = 'center',
  className = '',
}: SectionHeadingProps) {
  const alignClass = align === 'center' ? 'text-center items-center' : 'text-start items-start';
  return (
    <div className={`flex flex-col gap-3 ${alignClass} ${className}`.trim()}>
      {eyebrow && (
        <span className="badge badge-brand w-fit">{eyebrow}</span>
      )}
      <h2 className="text-3xl font-bold sm:text-4xl text-[var(--text-primary)]">{title}</h2>
      {description && (
        <p className="max-w-xl text-base text-[var(--text-secondary)]">{description}</p>
      )}
    </div>
  );
}
