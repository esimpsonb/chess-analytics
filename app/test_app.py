import streamlit as st
import chess.pgn
import chess.svg
from io import StringIO

st.title("♟️ Visor PGN con Flechas")

# PGN de ejemplo
pgn_text = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2023.06.15"]
[White "Hikaru Nakamura"]
[Black "Firouzja, Alireza"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6
8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7
14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6
20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7
25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5 hxg5 29. Rc1 c4
30. a3 b3 31. Re1 Na4 32. Re2 c3 33. bxc3 b2 34. Re1 Be4 35. f3 Bd3
36. Kf2 Nxc3 37. Ke3 b1=Q 38. Rxb1 Bxb1 39. Kd4 Ne2+ 40. Ke3 Nf4 41. g3 Nxh3
42. f4 gxf4+ 43. gxf4 Ke6 44. a4 Kd5 45. Kf3 Bf5 46. Kg3 Kc5 47. Kh4 Kb4
48. Kh5 Kxa4 49. Kh4 Kb4 50. Kg3 Kc3 51. Kf3 Kd3 52. Kg3 Ke3 53. Kh4 Kxf4
54. Kh5 g5 55. Kh6 g4 56. Kh5 g3 57. Kh4 g2 58. Kh5 g1=Q 59. Kh6 Qg6#
"""

pgn_text = '[Event "Live Chess"]\n[Site "Chess.com"]\n[Date "2025.09.02"]\n[Round "-"]\n[White "yesilikeorangejuice"]\n[Black "Hikaru"]\n[Result "0-1"]\n[Tournament "https://www.chess.com/tournament/live/titled-tuesday-blitz-september-02-2025-5905663"]\n[CurrentPosition "8/8/8/4p2B/1p1kP3/5P1p/1K6/3b4 w - - 0 61"]\n[Timezone "UTC"]\n[ECO "B06"]\n[ECOUrl "https://www.chess.com/openings/Modern-Defense-with-1-e4...3.Nf3-c6-4.Bd3-d6"]\n[UTCDate "2025.09.02"]\n[UTCTime "15:00:00"]\n[WhiteElo "2645"]\n[BlackElo "3400"]\n[TimeControl "300"]\n[Termination "Hikaru won by resignation"]\n[StartTime "15:00:00"]\n[EndDate "2025.09.02"]\n[EndTime "15:08:45"]\n[Link "https://www.chess.com/game/live/151138695137"]\n\n1. e4 1... g6 2. d4 2... Bg7 3. Nf3 3... c6 4. Bd3 4... d6 5. h3 5... Nf6 6. a4 6... a5 7. O-O 7... O-O 8. Nbd2 8... Qc7 9. Re1 9... e5 10. dxe5 10... dxe5 11. Nc4 11... Re8 12. b3 12... Na6 13. Bb2 13... Nd7 14. Ba3 14... Ndc5 15. Bf1 15... Rd8 16. Qc1 16... f6 17. Qe3 17... Bf8 18. Qc3 18... b6 19. Nfd2 19... Nb4 20. Ne3 20... Kg7 21. Bc4 21... Rd4 22. f3 22... Bb7 23. Rad1 23... Rad8 24. Ndf1 24... R8d7 25. Qa1 25... Qd8 26. c3 26... Rxd1 27. Rxd1 27... Rxd1 28. Qxd1 28... Qxd1 29. Nxd1 29... Nc2 30. Bc1 30... b5 31. axb5 31... cxb5 32. Bxb5 32... Nxb3 33. Bb2 33... Bc5+ 34. Kh1 34... Na3 35. Ba4 35... Ba6 36. Bxb3 36... Bxf1 37. Ne3 37... Bd3 38. Bxa3 38... Bxe3 39. c4 39... Bd2 40. c5 40... Bb4 41. Bxb4 41... axb4 42. c6 42... Bb5 43. c7 43... Bd7 44. Kg1 44... Kf8 45. Kf2 45... Ke7 46. Ke3 46... Kd6 47. h4 47... Kxc7 48. Bg8 48... h6 49. Kd3 49... Bb5+ 50. Kc2 50... Kb6 51. Kb3 51... Kc5 52. g3 52... g5 53. hxg5 53... fxg5 54. Be6 54... h5 55. Bf7 55... h4 56. gxh4 56... gxh4 57. Be6 57... Be2 58. Bg4 58... Bd1+ 59. Kb2 59... Kd4 60. Bh5 60... h3 0-1'

# Cargar partida
game = chess.pgn.read_game(StringIO(pgn_text))
board = game.board()
moves = list(game.mainline_moves())

# Inicializar estado
if "move_number" not in st.session_state:
    st.session_state.move_number = 0

# Avanzar jugadas
for move in moves[:st.session_state.move_number]:
    board.push(move)

# Última jugada para flecha y SAN
last_move = moves[st.session_state.move_number - 1] if st.session_state.move_number > 0 else None
arrows = []
if last_move:
    arrows = [(last_move.from_square, last_move.to_square)]


# Renderizar tablero
boardsvg = chess.svg.board(board=board, size=400, arrows=arrows)
st.write(boardsvg, unsafe_allow_html=True)

# Botones compactos debajo del tablero
cols = st.columns([0.2,0.2,0.2,0.2,2])  # los últimos 6 "empuja" los botones juntos
with cols[0]:
    if st.button("⏮️", key="start"):
        st.session_state.move_number = 0
with cols[1]:
    if st.button("⬅️", key="prev"):
        st.session_state.move_number = max(0, st.session_state.move_number - 1)
with cols[2]:
    if st.button("➡️", key="next"):
        st.session_state.move_number = min(len(moves), st.session_state.move_number + 1)
with cols[3]:
    if st.button("⏭️", key="end"):
        st.session_state.move_number = len(moves)


# Info
st.markdown(f"**Jugada:** {st.session_state.move_number}/{len(moves)}")
st.markdown(f"**Evento:** {game.headers.get('Event', '---')}")
st.markdown(f"**Blancas:** {game.headers.get('White', '---')}")
st.markdown(f"**Negras:** {game.headers.get('Black', '---')}")
st.markdown(f"**Resultado:** {game.headers.get('Result', '---')}")