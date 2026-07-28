export interface UserResponse {
  id: string;
  email: string;
  full_name: string | null;
  role: 'candidate' | 'recruiter' | 'admin';
  is_active: boolean;
}

export interface UserUpdate {
  full_name?: string;
}
