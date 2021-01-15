"""
MIT License

Copyright (c) 2020 UNKNOWN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import discord
from discord.ext import commands

import random

__PREFIX__ = 'YOUR_PREFIX'  # 원하는 접두사를 입력하세요.
__TOKEN__ = 'YOUR_TOKEN' # 당신이 생성한 봇 애플리케이션의 토큰을 붙여넣으세요.
COLOR = 0xFFFFFF    # 원하는 색깔을 지정하세요. (Embed 메시지 출력시 좌측에 표시되는 색깔입니다.) 반드시 HEX 코드로 작성하셔야 하며, 코드 앞에 0x를 기입해야 합니다.

bot = commands.Bot(command_prefix=__PREFIX__, case_insensitive=True)
# bot.remove_command("help") 이 구문은 help 명령어를 삭제할지 말지를 결정합니다. 삭제한다면 직접 만드실 수 있습니다.


@bot.event
async def on_ready():
    print(f'='*40 +
          f'\n{bot.user.name}(으)로 로그인합니다.'
          f'\n봇 ID: {bot.user.id}'
          f'\n접속중인 서버: {len(bot.guilds)}개\n'
          + f'=' * 40)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f'상태를 입력하세요.'))

    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return None
    
    
@bot.command(name='핑')
async def ping(ctx):
    embed = discord.Embed(title='지연시간', color=COLOR,
                          description=f'{int(round(bot.latency * 1000, 0))}ms')
    return await ctx.send(embed=embed)


@bot.command(name='프로필', aliases=['유저'])
async def profile(ctx, u: str = None):
    if not u:
        user = ctx.author
    else:
        try:
            user = await commands.MemberConverter().convert(ctx, u)
        except discord.ext.commands.errors.BadArgument:
            return await ctx.send(f'{u}(와)과 일치하는 유저의 이름을 찾을 수 없습니다.')
    embed = discord.Embed(title=f'{user.name}의 정보', color=user.color)
    embed.add_field(name='닉네임', value=user.mention, inline=False)
    embed.add_field(name='ID', value=user.id, inline=False)
    embed.add_field(name='최상위 역할', value=user.top_role.mention, inline=False)
    embed.add_field(name='상태', value=user.status, inline=False)
    joined_at = user.joined_at.strftime("%Y-%m-%d")
    embed.add_field(name='접속 일자', value=joined_at)
    embed.set_image(url=user.avatar_url)
    return await ctx.send(embed=embed)


@bot.command(name='서버')
async def server(ctx):
    embed = discord.Embed(title=f'`{ctx.guild}`의 정보', color=COLOR)
    embed.add_field(name='ID', value=ctx.guild.id, inline=False)
    embed.add_field(name='소유자', value=ctx.guild.owner.mention, inline=False)
    embed.add_field(name='역할', value=f'{len(ctx.guild.roles)}개', inline=True)
    embed.add_field(name='멤버', value=f'{len(ctx.guild.members)}명', inline=True)
    embed.add_field(name='지역', inline=True,
                    value=str(ctx.guild.region).upper().replace('-', ' '))
    embed.add_field(name='선호 언어', value=ctx.guild.preferred_locale, inline=True)
    embed.add_field(name='이모티콘 개수', inline=True,
                    value=f'{len(ctx.guild.emojis)}/{ctx.guild.emoji_limit * 2}')
    embed.add_field(name='부스트 레벨', value=ctx.guild.premium_tier, inline=True)
    embed.add_field(name='채널', inline=True, value=f'{len(ctx.guild.channels)}개')
    embed.add_field(name='음성 채널', inline=True, value=f'{len(ctx.guild.voice_channels)}개')
    embed.add_field(name='카테고리', inline=True, value=f'{len(ctx.guild.categories)}개')
    created_at = ctx.guild.created_at.strftime("%Y-%m-%d")
    embed.add_field(name='생성 일자', value=created_at, inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_image(url=ctx.guild.banner_url)
    return await ctx.send(embed=embed)


@bot.command(aliases=['주사위'])
async def dice(ctx):
    variable = str(random.randint(1,6))
    e = discord.Embed(title='주사위', color=COLOR,
                      description=f'{variable}(이)가 나왔습니다.')
    return await ctx.send(embed=e)


@bot.command(name='삭제', aliases=['제거'])
async def purge(ctx, limit: str = None):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send('권한이 부족합니다. `메시지 관리` 권한이 필요합니다.')
    if not limit:
        return await ctx.send('삭제할 메시지의 개수를 입력해주세요.')
    try:
        await ctx.channel.purge(limit=int(limit) + 1)  # 삭제할 메시지의 개수에 사용자가 전송한 명령어는 포함시키지 않기 위해 +1을 합니다.
    except ValueError:
        return await ctx.send('입력하신 값은 숫자가 아닙니다.')
    except discord.errors.Forbidden:
        return await ctx.send('봇의 권한이 부족합니다.')
    embed = discord.Embed(title='메시지 삭제 완료', color=COLOR,
                      description=f'{limit}개의 메시지가 삭제되었습니다.'
                                  f'\nBy: {ctx.author.mention}')
    return await ctx.send(embed=embed, delete_after=5)


@bot.command(name='추방', aliases=['킥'])
async def kick(ctx, user: str = None, *, reason: str = None):
    if not ctx.author.guild_permissions.kick_members:
        return await ctx.send('권한이 부족합니다. `멤버 추방하기` 권한이 필요합니다.')
    if not user:
        return await ctx.send('추방할 유저를 입력해주세요.')
    if reason is None:
        reason = '없음'
    try:
        member = await commands.MemberConverter().convert(ctx, user)
    except discord.ext.commands.errors.BadArgument:
        return await ctx.send(f'{user}(와)과 일치하는 유저를 찾을 수 없습니다.')
    try:
        await ctx.guild.kick(member, reason=reason)
    except discord.errors.Forbidden:
        return await ctx.send('봇의 권한이 부족합니다.')
    embed = discord.Embed(title='유저 추방 완료', color=COLOR,
                      description=f'{member.mention}(이)가 추방되었습니다.'
                                  f'\nBy: {ctx.author.mention}'
                                  f'\n사유: {reason}')
    return await ctx.send(ctx.author.mention, embed=embed)


@bot.command(name='차단', aliases=['밴'])
async def ban(ctx, user: str = None, *, reason: str = None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send('권한이 부족합니다. `멤버 차단하기` 권한이 필요합니다.')
    if not user:
        return await ctx.send('차단할 유저를 입력해주세요.')
    if reason is None:
        reason = '없음'
    try:
        member = await commands.MemberConverter().convert(ctx, user)
    except discord.ext.commands.errors.BadArgument:
        return await ctx.send(f'{user}(와)과 일치하는 유저를 찾을 수 없습니다.')
    try:
        await ctx.guild.ban(member, reason=reason)
    except discord.errors.Forbidden:
        return await ctx.send('봇의 권한이 부족합니다.')
    embed = discord.Embed(title='유저 차단 완료', color=COLOR,
                      description=f'{member.mention}(이)가 차단되었습니다.'
                                  f'\nBy: {ctx.author.mention}'
                                  f'\n사유: {reason}')
    return await ctx.send(ctx.author.mention, embed=embed)


@bot.command(name='공지')
async def announce(ctx, *, content: str = None):
    if not content:
        return await ctx.send("전송할 메시지를 입력주세요.")
    embed = discord.Embed(title='공지', description=content, color=COLOR)
    embed.set_footer(text=f"By: {ctx.author}")
    await ctx.send(embed=embed)


bot.run(__TOKEN__, bot=True, reconnect=True)
