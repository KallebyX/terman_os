import React from 'react';
import { Table } from '../ui';

interface Column<T> {
  key: keyof T | string;
  title: string;
  render?: (row: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
}

export function DataTable<T>({ data, columns, onRowClick }: DataTableProps<T>) {
  return (
    <Table>
      <Table.Head>
        <Table.Row>
          {columns.map((column) => (
            <Table.Cell key={column.key.toString()}>{column.title}</Table.Cell>
          ))}
        </Table.Row>
      </Table.Head>
      <Table.Body>
        {data.map((row, index) => (
          <Table.Row
            key={index}
            onClick={() => onRowClick?.(row)}
            className={onRowClick ? 'cursor-pointer hover:bg-gray-50' : ''}
          >
            {columns.map((column) => (
              <Table.Cell key={column.key.toString()}>
                {column.render
                  ? column.render(row)
                  : row[column.key as keyof T]?.toString()}
              </Table.Cell>
            ))}
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
} 