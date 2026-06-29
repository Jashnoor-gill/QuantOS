import React from 'react';

type SkeletonProps = {
  className?: string;
};

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={
        className ??
        'animate-pulse rounded bg-slate-800/70'
      }
    />
  );
}

export function SkeletonLine({ className }: SkeletonProps) {
  return (
    <div
      className={
        className ??
        'h-4 w-full animate-pulse rounded bg-slate-800/70'
      }
    />
  );
}

