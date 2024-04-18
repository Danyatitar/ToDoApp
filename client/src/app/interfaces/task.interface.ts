import { CategoryInterface } from './category.interface';
import { UserInterface } from './user.interface';

export enum Status {
  In_progress = 'in progress',
  Completed = 'completed',
  Waiting = 'waiting',
}

export interface TaskInterface {
  id?: string;
  title: string;
  description: string;
  deadline: Date;
  status: Status;
  category_id?: string | null | undefined;
  category?: CategoryInterface;
  user?: UserInterface;
  user_id?: string | null | undefined;
}
