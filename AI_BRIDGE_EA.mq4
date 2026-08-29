#property strict

//+------------------------------------------------------------------+
//| SEZIONE 1: CONFIGURAZIONE GENERALE (Modificabile da MT4)        |
//+------------------------------------------------------------------+
input string   General_Settings   = "=== Configurazione Generale ===";
input double   Min_Lot            = 0.01;   // Lotto minimo consentito
input double   Max_Lot            = 1.00;   // Lotto massimo consentito
input int      Magic_Number       = 1818;   // Identificativo ordini
input bool     Limit_One_Position = true;   // Blocca se c'è già un ordine aperto

//+------------------------------------------------------------------+
//| SEZIONE 2: GESTIONE RISCHIO (Modificabile da MT4)               |
//+------------------------------------------------------------------+
input string   Risk_Settings      = "=== Gestione Rischio ===";
input double   Stop_Loss_Pips     = 150;    // Stop Loss in pips (default 150)
input double   Take_Profit_Pips   = 1450;   // Take Profit in pips (default 1450)
input bool     Use_Fixed_Risk     = true;   // Usa SL/TP fissi dalla finestra? (Se false, usa quelli di Python)

//+------------------------------------------------------------------+
//| SEZIONE 3: FILTRO ORARIO (Modificabile da MT4)                  |
//+------------------------------------------------------------------+
input string   Time_Settings      = "=== Filtro Orario ===";
input bool     Enable_Time_Filter = true;   // Attiva filtro orario
input int      Start_Trade_Hour   = 8;      // Ora di inizio (0-23, es. 8 = Londra)
input int      Stop_Trade_Hour    = 22;     // Ora di fine (0-23, es. 22 = New York chiusura)

//+------------------------------------------------------------------+
//| VARIABILI INTERNE                                                |
//+------------------------------------------------------------------+
string cmd_file = "AI_BRIDGE_CMD.txt";
string res_file = "AI_BRIDGE_RES.txt";

//+------------------------------------------------------------------+
//| Funzione per normalizzare il lotto entro i limiti min/max       |
//+------------------------------------------------------------------+
double NormalizeLot(double lot)
{
   if(lot < Min_Lot) lot = Min_Lot;
   if(lot > Max_Lot) lot = Max_Lot;
   return NormalizeDouble(lot, 2);
}

//+------------------------------------------------------------------+
//| Funzione per contare le posizioni aperte (per il simbolo)       |
//+------------------------------------------------------------------+
int CountOpenPositions()
{
   int count = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderSymbol() == Symbol() && OrderMagicNumber() == Magic_Number)
         {
            count++;
         }
      }
   }
   return count;
}

//+------------------------------------------------------------------+
//| Funzione per verificare se siamo dentro l'orario di trading      |
//+------------------------------------------------------------------+
bool IsTradingTime()
{
   if(!Enable_Time_Filter) return(true);
   
   int current_hour = Hour();
   
   // Gestione orari che attraversano la mezzanotte (es. 22 -> 8)
   if(Start_Trade_Hour < Stop_Trade_Hour)
   {
      return(current_hour >= Start_Trade_Hour && current_hour < Stop_Trade_Hour);
   }
   else
   {
      // Es. dalle 22 alle 8 (Tokyo)
      return(current_hour >= Start_Trade_Hour || current_hour < Stop_Trade_Hour);
   }
}

//+------------------------------------------------------------------+
//| EVENTO PRINCIPALE ONTICK                                        |
//+------------------------------------------------------------------+
void OnTick()
{
   // 1. CONTROLLO ORARIO
   if(!IsTradingTime())
   {
      // Se fuori orario, elimina eventuali comandi in sospeso
      if(FileIsExist(cmd_file)) FileDelete(cmd_file);
      return;
   }

   // 2. CONTROLLO SICUREZZA: Se è attivo il limite di 1 posizione
   if(Limit_One_Position)
   {
      if(CountOpenPositions() >= 1)
      {
         if(FileIsExist(cmd_file)) FileDelete(cmd_file);
         return;
      }
   }

   // 3. LETTURA COMANDO DA PYTHON
   if(FileIsExist(cmd_file))
   {
      int handle = FileOpen(cmd_file, FILE_READ|FILE_TXT|FILE_ANSI);
      if(handle > 0)
      {
         string cmd = FileReadString(handle);
         FileClose(handle);
         
         // Elimina il file comando per non riprocessarlo
         FileDelete(cmd_file);

         // Formato atteso: ACTION,LOTS,SL_PIPS,TP_PIPS oppure ACTION,LOTS
         // Se il comando viene solo con ACTION e LOTS, usa i parametri della finestra per SL/TP
         
         string parts[];
         int split = StringSplit(cmd, ',', parts);
         
         if(split >= 2)
         {
            string action = parts[0];
            double lots = NormalizeLot(StringToDouble(parts[1]));
            
            // Default SL/TP dalla finestra
            double sl_pips = Stop_Loss_Pips;
            double tp_pips = Take_Profit_Pips;
            
            // Se Python invia SL/TP personalizzati (parti 3 e 4), usali
            if(split >= 4)
            {
               sl_pips = StringToDouble(parts[2]);
               tp_pips = StringToDouble(parts[3]);
            }
            
            // Calcola prezzi SL/TP
            double sl_price = 0;
            double tp_price = 0;
            double point = Point;
            double pip = (Digits == 3 || Digits == 5) ? point * 10 : point;
            
            int ticket = -1;
            
            if(action == "buy")
            {
               double current_price = Ask;
               sl_price = current_price - (sl_pips * pip);
               tp_price = current_price + (tp_pips * pip);
               ticket = OrderSend(Symbol(), OP_BUY, lots, current_price, 3, sl_price, tp_price, "AI_BRIDGE", Magic_Number, 0, clrBlue);
            }
            else if(action == "sell")
            {
               double current_price = Bid;
               sl_price = current_price + (sl_pips * pip);
               tp_price = current_price - (tp_pips * pip);
               ticket = OrderSend(Symbol(), OP_SELL, lots, current_price, 3, sl_price, tp_price, "AI_BRIDGE", Magic_Number, 0, clrRed);
            }
            
            // Scrivi risposta per Python
            int res_handle = FileOpen(res_file, FILE_WRITE|FILE_TXT|FILE_ANSI);
            if(res_handle > 0)
            {
               if(ticket > 0) FileWrite(res_handle, "OK:", ticket);
               else FileWrite(res_handle, "ERR:", GetLastError());
               FileClose(res_handle);
            }
         }
      }
   }
}
