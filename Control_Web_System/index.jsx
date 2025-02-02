// 대시보드 메인 페이지 구성 코드

import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import HourlyChart from "../../components/HourlyChart";
import React, { useState, useEffect } from 'react';
import api_key from "../../api_key.json";
import WeatherT from "./Weather";
import HourlyData from "./hourlyData";
import { Link } from 'react-router-dom';

import WeekChart from "../../components/WeekChart";



const Dashboard = () => {

  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [weather, setWeather] = useState(null);


  const columns = [
    { field: "id", headerName: "연번", flex: 0.5 },
    { field: "police_office", headerName: "경찰서" },
    { field: "name", headerName: "관서명", flex: 1, cellClassName: "name-column-cell" },
    { field: "division", headerName: "구분", headerAlign: "left", align: "left" },
    { field: "phone_number", headerName: "전화번호", flex: 1 },
    { field: "address", headerName: "주소", flex: 1 },
  ];

  const [data, setData] = useState([]); // useState 사용
  const stateRefresh = () => {
    // stateRefresh 함수 정의
    fetch('/api/customers')
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error(error));
      
  };

  useEffect(() => {
    stateRefresh(); // 컴포넌트가 로드될 때 데이터 불러오기
  }, []);

    return (
        <Box m = '20px' >
          <Box display = 'flex' justifyContent='space-between' alignItems="center">
            <Header title="DASHBOARD" subtitle="관제 상황과 통계를 볼 수 있는 메인 페이지입니다." />
          </Box>

          {/* GRID CHARTS */}
          <Box
            display="grid"
            gridTemplateColumns="repeat(12, 1fr)"
            gridAutoRows="140px"
            gap="20px"
            color={colors.grey[100]}
          >
            {/* ROW 1 */}
      
            <Box
          gridColumn="span 7"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          sx={{ }}>
          <WeatherT weather={weather} setWeather={setWeather} display="flex" />
        </Box>

              {/* TRANSACTIONS */}
              <Box 
                gridColumn="span 5" 
                gridRow="span 3" 
                backgroundColor = {colors.primary[400]}
                overflow="auto"
              >
                <Box 
                  display="flex" 
                  justifyContent="space-between" 
                  alignItems="center" 
                  borderBottom={`4px solid ${colors.primary[500]}`} 
                  colors={colors.grey[100]} 
                  p="15px"
                >
                  <Typography 
                    color={colors.greenAccent[500]}
                    variant="h4" 
                    fontWeight="600"
                    backgroundColor={colors.primary[400]}
                    display="flex"
                  >
                    금일 신고 데이터 확인 요청
                  </Typography>
                  <Link to="/faq" style={{ textDecoration: 'none' }}>
                  <Button
                    variant="contained"
                    color="secondary"
                    display="flex"
                    sx={{fontSize: "16px", fontWeight: "bold", backgroundColor: colors.blueAccent[600], color: "white"}}
                  >
                  페이지 이동
                </Button>
                </Link>
                </Box>
                  <Box 
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                    p="15px"
                    width="100%"
                  >
                    <Box>
                      <HourlyData />
                    </Box>
                  </Box>
              </Box>

              {/* ROW 3 */}
              <Box
  gridColumn="span 4"
  gridRow="span 2"
  backgroundColor={colors.primary[400]}
  p="30px"
>
  <Typography variant="h5" fontWeight="600">
    지난 주 대비 신고량 차트
  </Typography>
  <Box height="240px" width="100%">
    <WeekChart />
  </Box>
</Box>

        <Box
          gridColumn="span 8"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          padding="30px"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            하루 신고 시간대 차트
          </Typography>
          <Box height="230px" mt="1px" width="105%">
            <HourlyChart isDashboard={true} />
          </Box>
        </Box>
          </Box>
      </Box>
      
    );
};

export default Dashboard;
