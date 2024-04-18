import { UserInterface } from './user.interface';

export interface CategoryInterface {
  id: string;
  name: string;
  user?: UserInterface;
  user_id?: string;
}
