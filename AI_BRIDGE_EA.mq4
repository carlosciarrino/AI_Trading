//+------------------------------------------------------------------+
//|                                              AI_BRIDGE_EA.mq4   |
//|                                Progetto AI_BRIDGE - Bridge MT4   |
//+------------------------------------------------------------------+
#property strict

void OnTick()
{
   string cmd_file = "AI_BRIDGE_CMD.txt";
   string res_file = "AI_BRIDGE_RES.txt";
   string debug_file = "AI_BRIDGE_DEBUG.txt"; // File di log

   // Scrive nel log di debug per capire se l'EA sta girando
   int debug_handle = FileOpen(debug_file, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(debug_handle > 0)
   {
      FileWrite(debug_handle, "EA attivo, controllo comando...");
      FileClose(debug_handle);
   }

   // Se esiste un comando da eseguire
   if(FileIsExist(cmd_file))
   {
      int handle = FileOpen(cmd_file, FILE_READ|FILE_TXT|FILE_ANSI);
      if(handle > 0)
      {
         string cmd = FileReadString(handle);
         FileClose(handle);
         
         // Elimina il file comando per non riprocessarlo
         FileDelete(cmd_file);

         // Formato atteso: ACTION,LOTS,PRICE,SL,TP
         if(StringLen(cmd) > 5)
         {
            string parts[];
            int split = StringSplit(cmd, ',', parts);
            if(split == 5)
            {
               string action = parts[0];
               double lots = StringToDouble(parts[1]);
               double price = StringToDouble(parts[2]);
               double sl = StringToDouble(parts[3]);
               double tp = StringToDouble(parts[4]);

               int ticket = -1;
               double current_price = 0;
               color col = clrWhite;

               if(action == "buy")
               {
                  current_price = Ask;
                  col = clrBlue;
                  ticket = OrderSend(Symbol(), OP_BUY, lots, current_price, 3, sl, tp, "AI_BRIDGE", 0, 0, col);
               }
               else if(action == "sell")
               {
                  current_price = Bid;
                  col = clrRed;
                  ticket = OrderSend(Symbol(), OP_SELL, lots, current_price, 3, sl, tp, "AI_BRIDGE", 0, 0, col);
               }

               // Scrivi la risposta per Python
               int res_handle = FileOpen(res_file, FILE_WRITE|FILE_TXT|FILE_ANSI);
               if(res_handle > 0)
               {
                  if(ticket > 0)
                  {
                     FileWrite(res_handle, "OK:", ticket);
                  }
                  else
                  {
                     FileWrite(res_handle, "ERR:", GetLastError());
                  }
                  FileClose(res_handle);
               }
               else
               {
                  // Se non riesce a scrivere la risposta, scrive l'errore nel debug
                  int dbg = FileOpen(debug_file, FILE_WRITE|FILE_TXT|FILE_ANSI);
                  if(dbg > 0)
                  {
                     FileWrite(dbg, "ERRORE FileOpen risposta: ", GetLastError());
                     FileClose(dbg);
                  }
               }
            }
         }
      }
   }
}
