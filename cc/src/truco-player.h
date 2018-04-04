#include <array>
#include <vector>
#include <algorithm>
#include <set>
#include <random>

enum CardOrdering {
  EQ,
  LT,
  GT
};

enum EnvidoResponse {
  NO_QUIERO_E,
  ENVIDO0,
  ENVIDO1,
  REALENVIDO,
  FALTAENVIDO,
  QUIERO_E
};

enum TrucoLevel {
  NADA,
  TRUCO,
  RETRUCO,
  VALECUATRO
};

enum QuererResponse {
  NO_QUIERO,
  QUIERO
};

enum Palo {
  COPA,
  BASTO,
  ORO,
  ESPADA
};

class Card;
class GameState;



class TrucoPlayer {
 public:
  virtual size_t SayTanto() = 0;
  virtual EnvidoResponse CantarEnvido(const GameState& state) = 0;
  virtual EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses) = 0;
  virtual TrucoLevel CantarTruco(
      const GameState& state, TrucoLevel current_truco) = 0;
  virtual QuererResponse AnswerTruco(
      const GameState& state, TrucoLevel new_truco) = 0;
  virtual Card PlayCard(const GameState& state) = 0;
  virtual ~TrucoPlayer() { };
};

class DumbTrucoPlayer : public TrucoPlayer {
 public:
  DumbTrucoPlayer(std::string name) : name_(name) {}
  size_t SayTanto();
  EnvidoResponse CantarEnvido(const GameState& state);
  EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses);
  TrucoLevel CantarTruco(
      const GameState& state, TrucoLevel current_truco);
  QuererResponse AnswerTruco(
      const GameState& state, TrucoLevel new_truco);
  Card PlayCard(const GameState& state);
  ~DumbTrucoPlayer() {
  }
 private:
  std::string name_;
};

class HumanTrucoPlayer : public TrucoPlayer {
 public:
  size_t SayTanto();
  EnvidoResponse CantarEnvido(const GameState& state);
  EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses);
  TrucoLevel CantarTruco(const GameState& state, TrucoLevel current_truco);
  QuererResponse AnswerTruco(const GameState& state, TrucoLevel new_truco);
  Card PlayCard(const GameState& state);
};


