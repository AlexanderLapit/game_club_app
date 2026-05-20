from database import SessionLocal
from models.tournament import Tournament, TournamentParticipant, Match, TournamentStatus, MatchResult
from models.user import User
from datetime import datetime
import math
import random


class TournamentController:
    def __init__(self, session=None):
        self.db_session = session or SessionLocal()

    def create_tournament(self, name, game, start_date, max_participants, created_by, description="", prize_pool=""):
        """Создать новый турнир"""
        tournament = Tournament(
            name=name,
            game=game,
            description=description,
            start_date=start_date,
            max_participants=max_participants,
            prize_pool=prize_pool,
            created_by=created_by,
            created_at=datetime.now(),
            status=TournamentStatus.REGISTRATION
        )
        self.db_session.add(tournament)
        self.db_session.commit()
        return tournament

    def get_all_tournaments(self, status=None):
        """Получить все турниры с возможной фильтрацией по статусу"""
        query = self.db_session.query(Tournament)
        if status:
            query = query.filter(Tournament.status == status)
        return query.order_by(Tournament.start_date.desc()).all()

    def get_tournament_by_id(self, tournament_id):
        """Получить турнир по ID"""
        return self.db_session.query(Tournament).filter(Tournament.id == tournament_id).first()

    def register_participant(self, tournament_id, user_id):
        """Зарегистрировать участника на турнир"""
        tournament = self.get_tournament_by_id(tournament_id)

        if not tournament:
            raise ValueError("Турнир не найден")

        if tournament.status != TournamentStatus.REGISTRATION:
            raise ValueError("Регистрация на турнир закрыта")

        # Проверка количества участников
        participants_count = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id
        ).count()

        if participants_count >= tournament.max_participants:
            raise ValueError("Достигнуто максимальное количество участников")

        # Проверка, не зарегистрирован ли уже пользователь
        existing = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id,
            TournamentParticipant.user_id == user_id
        ).first()

        if existing:
            raise ValueError("Вы уже зарегистрированы на этот турнир")

        participant = TournamentParticipant(
            tournament_id=tournament_id,
            user_id=user_id,
            registered_at=datetime.now(),
            eliminated=False
        )

        self.db_session.add(participant)
        self.db_session.commit()
        return participant

    def unregister_participant(self, tournament_id, user_id):
        """Отменить регистрацию участника"""
        participant = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id,
            TournamentParticipant.user_id == user_id
        ).first()

        if not participant:
            raise ValueError("Регистрация не найдена")

        tournament = self.get_tournament_by_id(tournament_id)
        if tournament.status != TournamentStatus.REGISTRATION:
            raise ValueError("Нельзя отменить регистрацию после начала турнира")

        self.db_session.delete(participant)
        self.db_session.commit()

    def get_tournament_participants(self, tournament_id):
        """Получить список участников турнира"""
        return self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id
        ).join(User).order_by(TournamentParticipant.registered_at).all()

    def is_user_registered(self, tournament_id, user_id):
        """Проверить, зарегистрирован ли пользователь на турнир"""
        participant = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id,
            TournamentParticipant.user_id == user_id
        ).first()
        return participant is not None

    def generate_bracket(self, tournament_id):
        """Сгенерировать турнирную сетку (пары участников)"""
        tournament = self.get_tournament_by_id(tournament_id)
        if not tournament:
            raise ValueError("Турнир не найден")

        # Удаляем существующие матчи
        self.db_session.query(Match).filter(Match.tournament_id == tournament_id).delete()

        participants = self.get_tournament_participants(tournament_id)

        if len(participants) < 2:
            raise ValueError("Недостаточно участников для создания сетки")

        # Случайное перемешивание участников
        random.shuffle(participants)

        # Получаем ID участников
        participant_ids = [p.id for p in participants]
        total_participants = len(participant_ids)

        # Определяем количество раундов (округляем вверх до степени двойки)
        rounds = math.ceil(math.log2(total_participants))
        total_slots = 2 ** rounds  # Общее количество слотов в первом раунде
        byes = total_slots - total_participants  # Количество пустых мест

        print(f"Генерация сетки: участников={total_participants}, раундов={rounds}, слотов={total_slots}, bye={byes}")

        # Создаем структуру матчей для всех раундов
        matches_by_round = {}
        all_matches = []

        # Первый раунд: создаем матчи для всех слотов
        first_round_matches = []
        matches_in_first_round = total_slots // 2

        # Распределяем участников по матчам первого раунда
        # Игроки без соперника получают bye (автоматический проход)
        player_index = 0

        for match_num in range(1, matches_in_first_round + 1):
            player1_id = None
            player2_id = None

            # Первый игрок в паре
            if player_index < total_participants:
                player1_id = participant_ids[player_index]
                player_index += 1

            # Второй игрок в паре
            if player_index < total_participants:
                player2_id = participant_ids[player_index]
                player_index += 1

            match = Match(
                tournament_id=tournament_id,
                round_number=1,
                match_number=match_num,
                player1_id=player1_id,
                player2_id=player2_id,
                result=MatchResult.NOT_PLAYED
            )
            first_round_matches.append(match)
            all_matches.append(match)

            # Если только один игрок в матче - это bye
            if player1_id and not player2_id:
                print(f"Матч 1.{match_num}: игрок {player1_id} получает bye")
            elif player2_id and not player1_id:
                print(f"Матч 1.{match_num}: игрок {player2_id} получает bye (перемещен в player1)")
                # Перемещаем игрока в player1 для удобства
                match.player1_id = player2_id
                match.player2_id = None

        matches_by_round[1] = first_round_matches

        # Создаем матчи для последующих раундов
        current_round_matches = matches_in_first_round
        for round_num in range(2, rounds + 2):  # +2 для создания места под финал
            next_round_matches_count = math.ceil(current_round_matches / 2)
            round_matches = []

            for match_num in range(1, next_round_matches_count + 1):
                match = Match(
                    tournament_id=tournament_id,
                    round_number=round_num,
                    match_number=match_num,
                    result=MatchResult.NOT_PLAYED
                )
                round_matches.append(match)
                all_matches.append(match)

            matches_by_round[round_num] = round_matches
            current_round_matches = next_round_matches_count

            # Останавливаемся, когда дошли до финала (1 матч)
            if next_round_matches_count == 1:
                break

        # Сохраняем все матчи в БД
        for match in all_matches:
            self.db_session.add(match)

        self.db_session.commit()

        # Обрабатываем матчи первого раунда, где есть bye (только один игрок)
        self._process_auto_advancements(tournament_id, matches_by_round)

        tournament.status = TournamentStatus.ONGOING
        self.db_session.commit()

        return self.get_tournament_matches(tournament_id)

    def _process_auto_advancements(self, tournament_id, matches_by_round):
        """
        Обработать автоматические проходы (bye) в первом раунде.
        Игроки без соперника автоматически проходят во второй раунд.
        """
        first_round_matches = matches_by_round.get(1, [])

        for match in first_round_matches:
            # Если в матче только один игрок - это автоматический проход
            if match.player1_id and not match.player2_id:
                print(f"Автоматический проход для игрока {match.player1_id} из матча 1.{match.match_number}")

                # Отмечаем матч как завершенный победой player1
                match.result = MatchResult.PLAYER1_WIN
                match.winner_id = match.player1_id
                match.completed_at = datetime.now()

                # Продвигаем игрока в следующий раунд
                self._advance_to_next_round(tournament_id, match.match_number, match.winner_id, matches_by_round)
            elif match.player2_id and not match.player1_id:
                print(f"Автоматический проход для игрока {match.player2_id} из матча 1.{match.match_number}")

                # Отмечаем матч как завершенный победой player2
                match.result = MatchResult.PLAYER2_WIN
                match.winner_id = match.player2_id
                match.completed_at = datetime.now()

                # Продвигаем игрока в следующий раунд
                self._advance_to_next_round(tournament_id, match.match_number, match.winner_id, matches_by_round)

        self.db_session.commit()

    def _advance_to_next_round(self, tournament_id, current_match_num, winner_id, matches_by_round):
        """
        Продвинуть победителя в следующий раунд на основе номера матча.
        Матчи 1 и 2 -> Матч 1 следующего раунда
        Матчи 3 и 4 -> Матч 2 следующего раунда
        Нечетный матч -> player1, четный -> player2
        """
        # Определяем номер матча в следующем раунде
        next_match_num = (current_match_num + 1) // 2
        next_round = 2  # Всегда переходим во второй раунд из первого

        # Получаем матч следующего раунда
        next_round_matches = matches_by_round.get(next_round, [])

        # Ищем соответствующий матч
        target_match = None
        for match in next_round_matches:
            if match.match_number == next_match_num:
                target_match = match
                break

        if target_match:
            # Определяем позицию: нечетный матч -> player1, четный -> player2
            if current_match_num % 2 == 1:  # Нечетный номер
                target_match.player1_id = winner_id
                print(f"Победитель матча 1.{current_match_num} -> матч {next_round}.{next_match_num} как player1")
            else:  # Четный номер
                target_match.player2_id = winner_id
                print(f"Победитель матча 1.{current_match_num} -> матч {next_round}.{next_match_num} как player2")

            # Проверяем, готов ли матч к проведению
            if target_match.player1_id and target_match.player2_id:
                print(f"Матч {next_round}.{next_match_num} готов к проведению!")
        else:
            print(f"Предупреждение: не найден матч {next_round}.{next_match_num}")

    def get_tournament_matches(self, tournament_id, round_number=None):
        """Получить матчи турнира"""
        query = self.db_session.query(Match).filter(Match.tournament_id == tournament_id)
        if round_number:
            query = query.filter(Match.round_number == round_number)
        return query.order_by(Match.round_number, Match.match_number).all()

    def update_match_result(self, match_id, player1_score, player2_score, result):
        """Обновить результат матча и продвинуть победителя"""
        match = self.db_session.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Матч не найден")

        # Проверка, что оба игрока определены
        if not match.player1_id or not match.player2_id:
            raise ValueError("В матче не определены оба участника")

        # Проверка на ничью
        if player1_score == player2_score:
            raise ValueError("В турнире на выбывание не может быть ничьей")

        # Сохраняем результат
        match.player1_score = player1_score
        match.player2_score = player2_score
        match.completed_at = datetime.now()

        # Определяем победителя на основе результата
        if result == MatchResult.PLAYER1_WIN:
            match.result = MatchResult.PLAYER1_WIN
            match.winner_id = match.player1_id
            winner_id = match.player1_id
        elif result == MatchResult.PLAYER2_WIN:
            match.result = MatchResult.PLAYER2_WIN
            match.winner_id = match.player2_id
            winner_id = match.player2_id
        else:
            # На случай, если передан неверный статус - определяем по счету
            if player1_score > player2_score:
                match.result = MatchResult.PLAYER1_WIN
                match.winner_id = match.player1_id
                winner_id = match.player1_id
            else:
                match.result = MatchResult.PLAYER2_WIN
                match.winner_id = match.player2_id
                winner_id = match.player2_id

        self.db_session.commit()

        # Отмечаем проигравшего как выбывшего
        loser_id = match.player2_id if winner_id == match.player1_id else match.player1_id
        loser = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.id == loser_id
        ).first()
        if loser:
            loser.eliminated = True

        self.db_session.commit()

        # Продвигаем победителя в следующий раунд
        self._advance_winner_simple(match)

        # Проверяем, не завершен ли турнир
        self.check_tournament_completion(match.tournament_id)

    def _advance_winner_simple(self, match):
        """
        Простой метод продвижения победителя в следующий раунд.
        Основан на правиле: матчи 1 и 2 -> матч 1, матчи 3 и 4 -> матч 2 и т.д.
        Нечетный матч -> player1, четный -> player2
        """
        if not match.winner_id:
            print(f"Предупреждение: у матча {match.id} нет победителя")
            return

        next_round = match.round_number + 1

        # Ищем матч следующего раунда, куда должен попасть победитель
        next_match_num = (match.match_number + 1) // 2

        next_match = self.db_session.query(Match).filter(
            Match.tournament_id == match.tournament_id,
            Match.round_number == next_round,
            Match.match_number == next_match_num
        ).first()

        if not next_match:
            print(f"Матч {match.id} (раунд {match.round_number}, матч {match.match_number}) был финальным")
            return

        # Определяем позицию
        if match.match_number % 2 == 1:  # Нечетный матч -> player1
            next_match.player1_id = match.winner_id
            print(f"Победитель матча {match.round_number}.{match.match_number} -> "
                  f"матч {next_round}.{next_match_num} как player1")
        else:  # Четный матч -> player2
            next_match.player2_id = match.winner_id
            print(f"Победитель матча {match.round_number}.{match.match_number} -> "
                  f"матч {next_round}.{next_match_num} как player2")

        self.db_session.commit()

        # Проверяем, готов ли следующий матч
        if next_match.player1_id and next_match.player2_id:
            print(f"Матч {next_match.id} (раунд {next_round}, матч {next_match_num}) готов к проведению!")

    def check_tournament_completion(self, tournament_id):
        """Проверить, завершен ли турнир"""
        # Ищем финальный матч (максимальный раунд)
        final_match = self.db_session.query(Match).filter(
            Match.tournament_id == tournament_id
        ).order_by(Match.round_number.desc()).first()

        if final_match and final_match.result != MatchResult.NOT_PLAYED:
            tournament = self.get_tournament_by_id(tournament_id)
            tournament.status = TournamentStatus.COMPLETED
            tournament.completed_at = datetime.now()

            # Определяем итоговые места
            if final_match.winner_id:
                # Победитель турнира
                winner = self.db_session.query(TournamentParticipant).filter(
                    TournamentParticipant.id == final_match.winner_id
                ).first()
                if winner:
                    winner.final_position = 1

                # Финалист (проигравший в финале)
                loser_id = (final_match.player2_id if final_match.winner_id == final_match.player1_id
                            else final_match.player1_id)
                if loser_id:
                    loser = self.db_session.query(TournamentParticipant).filter(
                        TournamentParticipant.id == loser_id
                    ).first()
                    if loser:
                        loser.final_position = 2

            self.db_session.commit()
            print(f"Турнир {tournament_id} завершен! Победитель: participant_id={final_match.winner_id}")
            return True
        return False

    def delete_tournament(self, tournament_id):
        """Удалить турнир"""
        tournament = self.get_tournament_by_id(tournament_id)
        if tournament:
            self.db_session.delete(tournament)
            self.db_session.commit()

    def get_tournament_statistics(self, tournament_id):
        """Получить статистику турнира"""
        tournament = self.get_tournament_by_id(tournament_id)
        if not tournament:
            return None

        total_matches = self.db_session.query(Match).filter(
            Match.tournament_id == tournament_id
        ).count()

        completed_matches = self.db_session.query(Match).filter(
            Match.tournament_id == tournament_id,
            Match.result != MatchResult.NOT_PLAYED
        ).count()

        participants_count = self.db_session.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id
        ).count()

        return {
            'tournament': tournament,
            'total_matches': total_matches,
            'completed_matches': completed_matches,
            'participants_count': participants_count,
            'progress': (completed_matches / total_matches * 100) if total_matches > 0 else 0
        }

    def close(self):
        """Закрыть сессию"""
        if self.db_session:
            self.db_session.close()

    def __del__(self):
        self.close()