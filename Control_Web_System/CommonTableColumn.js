// 신고 기록 게시판 페이지 구성 컴포넌트 Column

import React from 'react';
import { Box, useTheme } from '@mui/system';
import { tokens } from '../../theme';

const CommonTableColumn = ({ children }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <td className="common-table-column">
      <Box sx={{ width: "100%"}}>
        <div className='columnPost'>
          {children}
        </div>
      </Box>
    </td>
  );
};

export default CommonTableColumn;
