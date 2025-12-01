"""
WebSocket Manager for Real-time Features
Handles battle rooms and interview sessions
"""

import socketio
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import json

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:3000', 'http://127.0.0.1:3000']
)


class BattleRoom:
    """Represents a code battle room"""
    
    def __init__(self, room_id: str, problem_id: int, time_limit: int = 900):
        self.room_id = room_id
        self.problem_id = problem_id
        self.time_limit = time_limit
        self.players: Dict[str, Dict] = {}  # sid -> player info
        self.status = "waiting"  # waiting, in_progress, completed
        self.started_at: Optional[datetime] = None
        self.winner: Optional[str] = None
    
    def add_player(self, sid: str, user_id: int, username: str):
        if len(self.players) < 2:
            self.players[sid] = {
                "user_id": user_id,
                "username": username,
                "progress": {"tests_passed": 0, "code_lines": 0, "attempts": 0},
                "submitted": False,
                "score": 0
            }
            return True
        return False
    
    def remove_player(self, sid: str):
        if sid in self.players:
            del self.players[sid]
    
    def is_full(self) -> bool:
        return len(self.players) >= 2
    
    def start(self):
        self.status = "in_progress"
        self.started_at = datetime.utcnow()
    
    def update_progress(self, sid: str, tests_passed: int, code_lines: int):
        if sid in self.players:
            self.players[sid]["progress"]["tests_passed"] = tests_passed
            self.players[sid]["progress"]["code_lines"] = code_lines
    
    def submit(self, sid: str, score: int, all_passed: bool):
        if sid in self.players:
            self.players[sid]["submitted"] = True
            self.players[sid]["score"] = score
            self.players[sid]["progress"]["attempts"] += 1
            
            if all_passed and not self.winner:
                self.winner = sid
                return True
        return False
    
    def get_time_remaining(self) -> int:
        if not self.started_at:
            return self.time_limit
        elapsed = (datetime.utcnow() - self.started_at).total_seconds()
        return max(0, int(self.time_limit - elapsed))
    
    def to_dict(self) -> Dict:
        return {
            "room_id": self.room_id,
            "problem_id": self.problem_id,
            "players": list(self.players.values()),
            "status": self.status,
            "time_remaining": self.get_time_remaining(),
            "winner": self.players.get(self.winner, {}).get("username") if self.winner else None
        }


class BattleManager:
    """Manages all battle rooms"""
    
    def __init__(self):
        self.rooms: Dict[str, BattleRoom] = {}
        self.player_rooms: Dict[str, str] = {}  # sid -> room_id
        self.waiting_queue: List[str] = []  # sids waiting for match
    
    def create_room(self, room_id: str, problem_id: int, time_limit: int = 900) -> BattleRoom:
        room = BattleRoom(room_id, problem_id, time_limit)
        self.rooms[room_id] = room
        return room
    
    def get_room(self, room_id: str) -> Optional[BattleRoom]:
        return self.rooms.get(room_id)
    
    def get_player_room(self, sid: str) -> Optional[BattleRoom]:
        room_id = self.player_rooms.get(sid)
        return self.rooms.get(room_id) if room_id else None
    
    def join_room(self, sid: str, room_id: str, user_id: int, username: str) -> bool:
        room = self.rooms.get(room_id)
        if room and room.add_player(sid, user_id, username):
            self.player_rooms[sid] = room_id
            return True
        return False
    
    def leave_room(self, sid: str):
        room_id = self.player_rooms.pop(sid, None)
        if room_id and room_id in self.rooms:
            self.rooms[room_id].remove_player(sid)
            # Clean up empty rooms
            if not self.rooms[room_id].players:
                del self.rooms[room_id]
    
    def add_to_queue(self, sid: str):
        if sid not in self.waiting_queue:
            self.waiting_queue.append(sid)
    
    def remove_from_queue(self, sid: str):
        if sid in self.waiting_queue:
            self.waiting_queue.remove(sid)
    
    def find_match(self, sid: str) -> Optional[str]:
        """Find an opponent from the waiting queue"""
        for other_sid in self.waiting_queue:
            if other_sid != sid:
                self.waiting_queue.remove(other_sid)
                return other_sid
        return None


# Global battle manager
battle_manager = BattleManager()


# Socket.IO Event Handlers

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    battle_manager.remove_from_queue(sid)
    room = battle_manager.get_player_room(sid)
    if room:
        battle_manager.leave_room(sid)
        # Notify other player
        await sio.emit('opponent_left', room.to_dict(), room=room.room_id)


@sio.event
async def join_battle(sid, data):
    """Join or create a battle room"""
    user_id = data.get("user_id")
    username = data.get("username")
    room_id = data.get("room_id")
    problem_id = data.get("problem_id", 1)
    
    if room_id:
        # Join existing room
        room = battle_manager.get_room(room_id)
        if room and battle_manager.join_room(sid, room_id, user_id, username):
            await sio.enter_room(sid, room_id)
            await sio.emit('battle_joined', room.to_dict(), room=room_id)
            
            # Start battle if room is full
            if room.is_full():
                room.start()
                await sio.emit('battle_start', room.to_dict(), room=room_id)
        else:
            await sio.emit('error', {"message": "Could not join room"}, to=sid)
    else:
        # Quick match - find opponent
        opponent_sid = battle_manager.find_match(sid)
        if opponent_sid:
            # Create room with both players
            import uuid
            new_room_id = str(uuid.uuid4())[:8]
            room = battle_manager.create_room(new_room_id, problem_id)
            
            # Get opponent info from their session
            battle_manager.join_room(sid, new_room_id, user_id, username)
            await sio.enter_room(sid, new_room_id)
            
            # Opponent joins too
            await sio.enter_room(opponent_sid, new_room_id)
            
            room.start()
            await sio.emit('battle_matched', room.to_dict(), room=new_room_id)
        else:
            # Add to queue
            battle_manager.add_to_queue(sid)
            await sio.emit('waiting_for_match', {"message": "Waiting for opponent..."}, to=sid)


@sio.event
async def update_progress(sid, data):
    """Update battle progress"""
    room = battle_manager.get_player_room(sid)
    if room:
        room.update_progress(
            sid,
            data.get("tests_passed", 0),
            data.get("code_lines", 0)
        )
        # Broadcast progress to room (anonymized for opponent)
        progress_update = {
            "players": [
                {
                    "username": p["username"],
                    "progress": p["progress"] if s == sid else {"tests_passed": p["progress"]["tests_passed"]}
                }
                for s, p in room.players.items()
            ]
        }
        await sio.emit('progress_update', progress_update, room=room.room_id)


@sio.event
async def submit_solution(sid, data):
    """Submit battle solution"""
    room = battle_manager.get_player_room(sid)
    if room:
        score = data.get("score", 0)
        all_passed = data.get("all_passed", False)
        
        is_winner = room.submit(sid, score, all_passed)
        
        if is_winner:
            room.status = "completed"
            await sio.emit('battle_end', room.to_dict(), room=room.room_id)
        else:
            await sio.emit('submission_result', {
                "passed": all_passed,
                "score": score
            }, to=sid)


@sio.event
async def leave_battle(sid, data):
    """Leave battle room"""
    room = battle_manager.get_player_room(sid)
    if room:
        await sio.leave_room(sid, room.room_id)
        battle_manager.leave_room(sid)
        await sio.emit('player_left', room.to_dict(), room=room.room_id)


# Interview session handlers

@sio.event
async def join_interview(sid, data):
    """Join an interview session"""
    interview_id = data.get("interview_id")
    await sio.enter_room(sid, f"interview_{interview_id}")
    await sio.emit('interview_joined', {"interview_id": interview_id}, to=sid)


@sio.event
async def interview_message(sid, data):
    """Send message in interview"""
    interview_id = data.get("interview_id")
    message = data.get("message")
    code = data.get("code")
    
    # Process with AI service (this would be done via API normally)
    await sio.emit('interviewer_typing', {"status": True}, to=sid)
    
    # Simulate AI response delay
    await asyncio.sleep(1)
    
    await sio.emit('interviewer_typing', {"status": False}, to=sid)
    await sio.emit('interviewer_message', {
        "content": "收到你的消息了。继续加油！",
        "timestamp": datetime.utcnow().isoformat()
    }, to=sid)

