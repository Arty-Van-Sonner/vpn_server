import { useState } from "react";
import {
  Alert,
  AppBar,
  Box,
  Button,
  Container,
  Paper,
  Stack,
  Tab,
  Tabs,
  TextField,
  Toolbar,
  Typography
} from "@mui/material";
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";

import { getNodes, getSessions, getUsers, login, Node, Session, setToken, User } from "./api";

const queryClient = new QueryClient();

const DataTable = <T extends Record<string, unknown>>({ title, rows }: { title: string; rows: T[] }) => {
  const keys = rows.length ? Object.keys(rows[0]) : [];
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        {title}
      </Typography>
      {rows.length === 0 ? (
        <Typography color="text.secondary">No data available</Typography>
      ) : (
        <Box sx={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {keys.map((key) => (
                  <th key={key} style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: "8px" }}>
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={idx}>
                  {keys.map((key) => (
                    <td key={key} style={{ borderBottom: "1px solid #f0f0f0", padding: "8px" }}>
                      {String(row[key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
      )}
    </Paper>
  );
};

const Dashboard = () => {
  const [tab, setTab] = useState(0);
  const users = useQuery<User[]>({ queryKey: ["users"], queryFn: getUsers });
  const nodes = useQuery<Node[]>({ queryKey: ["nodes"], queryFn: getNodes });
  const sessions = useQuery<Session[]>({ queryKey: ["sessions"], queryFn: getSessions });

  const commonError = users.error || nodes.error || sessions.error;
  const loading = users.isLoading || nodes.isLoading || sessions.isLoading;

  return (
    <Stack spacing={2}>
      <Tabs value={tab} onChange={(_, value) => setTab(value)}>
        <Tab label="Users" />
        <Tab label="Nodes" />
        <Tab label="Sessions" />
      </Tabs>
      {commonError && <Alert severity="error">Failed to load API data. Check backend auth and permissions.</Alert>}
      {loading && <Alert severity="info">Loading data...</Alert>}
      {tab === 0 && <DataTable title="Users" rows={users.data ?? []} />}
      {tab === 1 && <DataTable title="Nodes" rows={nodes.data ?? []} />}
      {tab === 2 && <DataTable title="Sessions" rows={sessions.data ?? []} />}
    </Stack>
  );
};

const AppBody = () => {
  const [email, setEmail] = useState("admin@vpn.local");
  const [password, setPassword] = useState("admin123");
  const [token, setAuthToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    setError(null);
    try {
      const accessToken = await login(email, password);
      setToken(accessToken);
      setAuthToken(accessToken);
    } catch {
      setError("Login failed");
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f7f8fc" }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">VPN Admin Panel</Typography>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 4 }}>
        {!token ? (
          <Paper sx={{ maxWidth: 420, mx: "auto", p: 3 }}>
            <Stack spacing={2}>
              <Typography variant="h6">Sign In</Typography>
              {error && <Alert severity="error">{error}</Alert>}
              <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
              <TextField
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button variant="contained" onClick={handleLogin}>
                Login
              </Button>
            </Stack>
          </Paper>
        ) : (
          <Dashboard />
        )}
      </Container>
    </Box>
  );
};

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppBody />
    </QueryClientProvider>
  );
}

