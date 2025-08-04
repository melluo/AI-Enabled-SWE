import React from 'react';
import { Box, Card, CardContent, TextField, Typography, Button, FormControl, InputLabel, Select, MenuItem, Grid } from '@mui/material';

const AffirmationLogging = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        minWidth: '100vw',
        bgcolor: '#f3f0ff',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        py: 4
      }}
    >
      <Box>
        <Card sx={{ mb: 4, p: 3, boxShadow: 3 }}>
          <CardContent>
            <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold', color: '#44337a', textAlign: 'center' }}>
              Affirmation Logging
            </Typography>
            <TextField
              fullWidth
              label="Affirmation Message"
              defaultValue="I am worthy of good things"
              variant="outlined"
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth variant="outlined" sx={{ mb: 2 }}>
              <InputLabel>Category</InputLabel>
              <Select defaultValue="Self-Esteem" label="Category">
                <MenuItem value="Self-Esteem">Self-Esteem</MenuItem>
                <MenuItem value="Positivity">Positivity</MenuItem>
                <MenuItem value="Empowerment">Empowerment</MenuItem>
                <MenuItem value="Motivation">Motivation</MenuItem>
              </Select>
            </FormControl>
            <Button
              fullWidth
              variant="contained"
              sx={{ bgcolor: '#6b46c1', ':hover': { bgcolor: '#553c9a' } }}
            >
              Submit
            </Button>
          </CardContent>
        </Card>

        <Card sx={{ boxShadow: 3 }}>
          <CardContent>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', color: '#44337a', textAlign: 'center' }}>
              Past Affirmations
            </Typography>
            <Grid container spacing={2}>
              <AffirmationCard message="I believe in myself" category="Self-Esteem" />
              <AffirmationCard message="I am grateful for today" category="Positivity" />
              <AffirmationCard message="I have the power to change" category="Empowerment" />
              <AffirmationCard message="I am doing my best" category="Motivation" />
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

const AffirmationCard = ({ message, category }) => (
  <Grid item xs={12} md={6}>
    <Card variant="outlined" sx={{ p: 2, borderColor: '#e2e8f0' }}>
      <Typography sx={{ fontWeight: 'bold', color: '#1a202c', mb: 1 }}>{message}</Typography>
      <Typography sx={{ color: '#718096' }}>{category}</Typography>
    </Card>
  </Grid>
);

export default AffirmationLogging;