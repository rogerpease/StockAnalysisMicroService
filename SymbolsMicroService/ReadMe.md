# Background

This is a simple microservice to list out stock symbol names. 

Usage:

% make dockerinstall
% wget -O - -q http://localhost:7000/rest/v1/SymbolNames
Returns: ['ABCD','EFGH',...] 
