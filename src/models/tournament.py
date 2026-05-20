from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database.db import Base
import enum


class TournamentStatus(enum.Enum):
    """Статус турнира"""
    REGISTRATION = "registration"  # Регистрация открыта
    ONGOING = "ongoing"  # Турнир идет
    COMPLETED = "completed"  # Турнир завершен
    CANCELLED = "cancelled"  # Турнир отменен


class MatchResult(enum.Enum):
    """Результат матча"""
    PLAYER1_WIN = "player1_win"
    PLAYER2_WIN = "player2_win"
    DRAW = "draw"
    NOT_PLAYED = "not_played"


class Tournament(Base):
    """Модель турнира"""
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    game = Column(String(100), nullable=False)
    description = Column(String(500))
    start_date = Column(DateTime, nullable=False)
    max_participants = Column(Integer, nullable=False)
    status = Column(Enum(TournamentStatus), default=TournamentStatus.REGISTRATION)
    prize_pool = Column(String(500))  # Описание призов
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)

    # Связи
    creator = relationship("User", back_populates="created_tournaments")
    participants = relationship("TournamentParticipant", back_populates="tournament", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="tournament", cascade="all, delete-orphan")


class TournamentParticipant(Base):
    """Участники турнира"""
    __tablename__ = "tournament_participants"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, nullable=False)
    seed = Column(Integer)  # Посев (для жеребьевки)
    eliminated = Column(Boolean, default=False)  # Выбыл из турнира
    final_position = Column(Integer)  # Итоговое место

    # Связи
    tournament = relationship("Tournament", back_populates="participants")
    user = relationship("User", back_populates="tournament_participations")
    matches_as_player1 = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    matches_as_winner = relationship("Match", foreign_keys="Match.winner_id", back_populates="winner")


class Match(Base):
    """Матчи турнира"""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    round_number = Column(Integer, nullable=False)  # Номер тура
    match_number = Column(Integer, nullable=False)  # Номер матча в туре

    player1_id = Column(Integer, ForeignKey("tournament_participants.id"))
    player2_id = Column(Integer, ForeignKey("tournament_participants.id"))

    player1_score = Column(Integer)
    player2_score = Column(Integer)

    result = Column(Enum(MatchResult), default=MatchResult.NOT_PLAYED)
    winner_id = Column(Integer, ForeignKey("tournament_participants.id"))

    scheduled_time = Column(DateTime)  # Запланированное время матча
    completed_at = Column(DateTime)  # Время завершения

    # Связи
    tournament = relationship("Tournament", back_populates="matches")
    player1 = relationship("TournamentParticipant", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("TournamentParticipant", foreign_keys=[player2_id], back_populates="matches_as_player2")
    winner = relationship("TournamentParticipant", foreign_keys=[winner_id], back_populates="matches_as_winner")