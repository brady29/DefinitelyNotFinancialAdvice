import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { blue } from '@mui/material/colors';

const bull = (
  <Box
    component="span"
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

export default function TruthTable(truths) {

    // const truthArray = truths["truths"]["truths"];
    let date = new Date();
    const truthArray = [
        {
            "created_at" : date.toJSON(),
            "text" : "sample text",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 2",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 3",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 4",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 5",
        }
    ]

    const theme = createTheme({
        palette: {
            secondary: blue,
        },
    });

    console.log(truthArray);

    return (
        <>
            <h1>Trump's Truths</h1>
            <div className="truth">
                <ThemeProvider theme={theme}>
                {truthArray.map((element, index) => (
                    <Card key={index} className="cards" sx={{ minWidth: 275 }}>
                        <CardContent>
                            <Typography gutterBottom sx={{ fontSize: 14 }}>
                            {Date(element["created_at"])}
                            </Typography>
                            <Typography variant="body2">
                                {element["text"]}
                            </Typography>
                        </CardContent>
                        <CardActions>
                            <Button color="secondary" size="small">Learn More</Button>
                        </CardActions>
                    </Card>
                ))}
                </ThemeProvider>
            </div>
        </>
    );
}