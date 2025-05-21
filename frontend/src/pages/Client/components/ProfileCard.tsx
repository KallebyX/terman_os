import React from 'react';
import { Card, Button } from '../../../components/ui';
import { User } from '../../../types';

interface ProfileCardProps {
  user: User;
  onEdit: () => void;
}

export const ProfileCard: React.FC<ProfileCardProps> = ({ user, onEdit }) => (
  <Card className="p-6">
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-lg font-medium">Perfil</h2>
      <Button variant="outline" onClick={onEdit}>
        Editar Perfil
      </Button>
    </div>
    <div className="space-y-4">
      <div>
        <label className="text-sm text-gray-500">Nome</label>
        <p className="font-medium">{user.name}</p>
      </div>
      <div>
        <label className="text-sm text-gray-500">E-mail</label>
        <p className="font-medium">{user.email}</p>
      </div>
      <div>
        <label className="text-sm text-gray-500">Telefone</label>
        <p className="font-medium">{user.phone || '-'}</p>
      </div>
      <div>
        <label className="text-sm text-gray-500">CPF/CNPJ</label>
        <p className="font-medium">{user.document || '-'}</p>
      </div>
    </div>
  </Card>
); 