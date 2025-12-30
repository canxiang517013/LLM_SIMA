/** TypeScript类型定义 */

// 消息类型
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  data?: any;
  dataType?: 'text' | 'table' | 'chart';
}

// 聊天请求
export interface ChatRequest {
  message: string;
  conversation_history?: Array<{ role: string; content: string }>;
  admin_token?: string;
}

// 聊天响应
export interface ChatResponse {
  success: boolean;
  message: string;
  data?: any;
  data_type?: string;
}

// 学生信息
export interface Student {
  id: number;
  name: string;
  student_id: string;
  class_name: string;
  college: string;
  major: string;
  grade: string;
  gender: '男' | '女';
  phone?: string;
  created_at?: string;
  updated_at?: string;
}
