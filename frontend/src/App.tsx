/** 主应用组件 */
import React, { useState } from 'react';
import { Layout, Input, Button, Card, Typography, Divider } from 'antd';
import { SendOutlined, ClearOutlined } from '@ant-design/icons';
import { Message, ChatRequest } from './types';
import { chat } from './services/api';
import MessageList from './components/MessageList';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [adminToken, setAdminToken] = useState('');

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const request: ChatRequest = {
        message: input,
        conversation_history: messages.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
        admin_token: adminToken || undefined,
      };

      const response = await chat(request);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        data: response.data,
        dataType: (response.data_type as 'text' | 'table' | 'chart') || 'text',
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，发生错误，请稍后重试。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 50px' }}>
        <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
          <Title level={3} style={{ color: '#fff', margin: 0 }}>
            学生信息管理助手
          </Title>
        </div>
      </Header>

      <Content style={{ padding: '24px 50px', background: '#f0f2f5' }}>
        <Card style={{ maxWidth: 1000, margin: '0 auto' }}>
          <div style={{ marginBottom: 16 }}>
            <Paragraph type="secondary">
              💡 提示：您可以用自然语言查询学生信息，例如：
            </Paragraph>
            <ul style={{ fontSize: 12, color: '#666' }}>
              <li>"查询所有计算机学院的学生"</li>
              <li>"统计每个年级的学生人数"</li>
              <li>"查询男女生的人数"</li>
              <li>"添加学生：张三，学号2025001..."（需要管理员令牌）</li>
            </ul>
            <Divider />
          </div>

          <div
            style={{
              height: '500px',
              overflowY: 'auto',
              marginBottom: 16,
              padding: '0 16px',
            }}
          >
            <MessageList messages={messages} />
          </div>

          <div style={{ marginBottom: 12 }}>
            <Input.Password
              placeholder="管理员令牌（可选，用于增删改操作）"
              value={adminToken}
              onChange={(e) => setAdminToken(e.target.value)}
              style={{ marginBottom: 8 }}
            />
          </div>

          <div style={{ display: 'flex', gap: 8 }}>
            <Input.TextArea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="请输入您的问题或指令..."
              autoSize={{ minRows: 2, maxRows: 6 }}
              disabled={loading}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              loading={loading}
              style={{ height: 'auto', alignSelf: 'flex-end' }}
            >
              发送
            </Button>
            <Button
              icon={<ClearOutlined />}
              onClick={handleClear}
              style={{ height: 'auto', alignSelf: 'flex-end' }}
            >
              清空
            </Button>
          </div>
        </Card>
      </Content>

      <Footer style={{ textAlign: 'center' }}>
        学生信息管理助手 ©{new Date().getFullYear()} Created with DeepSeek LLM
      </Footer>
    </Layout>
  );
}

export default App;
